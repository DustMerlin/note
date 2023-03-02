# bug#189247

## 问题分析：

    从现象很容易想象到，这又是kernel的处理仅针对了初始化的操作
    而在其他情况更新的源的时候，并未有额外的处理

    处理显示kernel 这块的逻辑，再 _reset_repo_store() 这个函数
    此前有所了解，但是找到这块，还是不得不粗略的看一遍代码

    测试现象： 在取消勾选和勾选 appstream 的时候，源均被更新，且 appstream 被去除和替换了

    当前分析结论：appsteam 源的更新是正常的，仅需在appstream 处理完成后再出发处理kernel 即可

    不难想象，但此时又很容易循环调用，导致死循环，但具体情况得测试了才能确定，目前还不能肯定
    以上情况，是最近每次改动内核所不得不面对的问题，每次尽量在规避，但还是会造成非常多的困扰
    也暂时没有更好的办法，以目前所要求的内容，去解耦合的实现，需求和代码设计层次上的矛盾
    ！ 暂时理论上应该无解

    此时可以想象，source 源选择的逻辑，是在选择后按照列表的规则，去重新加载所有的源
    而此时的矛盾是，可能是按当前列表里的源存在与否剔除相应的源,比如都选则不做处理，如果不勾选则剔除
    是符合现象，且合理的猜测，此处需要查看代码验证！！！

    _reset_repo_store() 对kernel的处理，存在破坏原有逻辑的问题，按上述逻辑，
    被剔除的kernel其实脱离了此部分代码的控制（数据被移除），且加载源的部分，并无从得知该情况，
    仅仅负责加载所有的源，导致出现上述的情况，以上猜想目前逻辑自洽

    单独但又些许关联影响的问题(一)：原先以数量判断源，导致如果appsteam不存在，源的数量不足，依旧不会出发kernel更新的操作
    现象是，/tmp/dnf.cache 中有两个kernel，但在此时如果在软件选择中选择kernel,并不会导致kernel切换

    appstream 也就是当前bug的问题和问题（一），不是同一个问题的推断依据
    此处可能都不是走的同一个流程
    appsteam 被取消勾选之后，/tmp/dnf.cache中只有两个kernel，此现象并不能看出什么情况来
    但是重新勾选appseam，/tmp/dnf.cache 有三个源，此情况是可以触发源过多而剔除kernel的操作的，但是并没有触发，所以该执行过程不同

    侵入式的现象验证，直接删除/tmp/dnf.cache 中的kernel观察现象：
        情况一：如果删除kernel后依旧出现，则证明所有源被重新加载，在重新加载过程中，appsteam 被处理了（保留或是删除，根据勾选情况）
        情况二：如果删除kernel后，kernel源不再出现，则证明此过程，没有所有源的重新加载，仅对appsteam，也即仅对列表中存在的appsteam 做处理

    但以上的思考是多余的，appsteam 被去除勾选之后，kernel 均被加载，且没被处理，该情况即可验证当前的所有猜想

    经过验证，猜想一是正确的，且dnf.cache下的文件被全部更新，即所有源被重新加载了

    通过源个数，处理kernel部分的逻辑，修正为通过kernel源个数判断后
    测试appstream取消勾选以后，依旧含有两个kernel源
    可证明，software_selection 中，对kernel 处理，不影响此部分的代码逻辑，但该关联问题，会影响后续的测试解决
    在本次修改中会讲此处的逻辑修正

    经过验证，修正后的代码，kernel的切换不影响，appstream的状态，一切正常

>   ！所以目前仅需将appstream勾选状态转变后，重新加载源时，想办法对kernel进行真确的处理即可
    
## 修改思路：

    找到appsteam更新后，更新源操作的部分，类似的像appsteam把除了当前kernel 的源剔除了
    但是如何确定，也即如何获取当前的kernel 好像也是问题

    或者通知soft_selection 的spokes 去 处理kernel 更合理

    暂时按以上两种思路验证

## installation_source.py 代码分析

从一些切入点依次排查，而非像上次依次分析绝大多数代码的功能作用
此次修改思路已经有了，问题的大概方向也基本上确定了，所以可以使用此种方式快速排查

上次的bug 是在快速排查无果之后，对源码进行分析，对可能的代码进行测试修改

> 去除源中kernel的操作

    !!  该操作过程中，或许应该在单独的变量中保留kernel状态，在soft_selection 状态切换时做切换（逻辑疑似合理）
        并且修改该变量，在appsteam 变更后，同步kernel 的不可见状态，
        或者说把不需要的kernel 设置成如同appsteam 不被勾选的状态，即enabled=False
        但这种方式，也有不合理之处，可能会影响显示
        第二种方式，在payload 的enabled状态设置为False ,可能appsteam 便是如此设置的，待看代码考证

``` python
    def _reset_repo_store(self):
        """ Reset the list of repos.

            Populate the list with all the addon repos from payload.addons.

            If the list has no element, clear the repo entry fields.
        """

        log.debug("Clearing checks in source spoke")

        # Remove the repo checks
        for checks in self._repo_checks.values():
            self.remove_check(checks.name_check)
            self.remove_check(checks.url_check)
            self.remove_check(checks.proxy_check)
        self._repo_checks = {}

        with self._repo_store_lock:
            self._repo_store.clear()
            repos = self.payload.addons
            log.debug("Setting up repos: %s", repos)
            for name in repos:
                repo = self.payload.get_addon_repo(name)
                ks_repo = self.data.RepoData.create_copy(repo)
                # Track the original name, user may change .name
                ks_repo.orig_name = name
                # Add addon repository id for identification
                ks_repo.repo_id = next(self._repo_counter)
                if name not in self._kernel_repos:
                    # 将非kernel的name，即appstream 源添加到 _repo_store中
                    self._repo_store.append([self.payload.is_repo_enabled(name),
                                            ks_repo.name,
                                            ks_repo])

        if len(self._repo_store) > 0:
            self._repo_selection.select_path(0)
        else:
            self._clear_repo_info()
            self._repo_entry_box.set_sensitive(False)
```

kernel 在

> repoStore

    从图形界面确定相应功能的组件，找到对应的glade文件中的id和绑定的相关的handle函数

    <object class="GtkListStore" id="repoStore">

    <signal name="row-changed" handler="on_repoStore_row_changed" swapped="no"/>
    <signal name="row-deleted" handler="on_repoStore_row_deleted" swapped="no"/>
    <signal name="row-inserted" handler="on_repoStore_row_inserted" swapped="no"/>

> on_repoStore_row_changed 

``` python
    def on_repoStore_row_changed(self, model, path, itr, user_data=None):
        self._duplicate_repo_check.update_check_status()

        repo = model[itr][REPO_OBJ]
        self._update_file_protocol(repo)
```

> on_repoStore_row_deleted

``` python
    def on_repoStore_row_deleted(self, model, path, user_data=None):
        self._duplicate_repo_check.update_check_status()
```

> on_repoStore_row_inserted

``` python
    def on_repoStore_row_inserted(self, model, path, itr, user_data=None):
        self._duplicate_repo_check.update_check_status()

        repo = model[itr][REPO_OBJ]

        # Add checks for the repo fields
        # Use InputCheckHandler.add_check instead of GUISpokeInputCheckHandler.add_check since
        # the input fields are used by every repo, so the changed signal handler is shared by
        # more than one check and needs to update only the active one.

        # It would be nice if we could store itr as the means of accessing this row later,
        # and GtkListStore sets GTK_TREE_MODEL_ITERS_PERSIST which is supposed to let us
        # do something like that, but as part of a grand practical joke the iter passed in
        # to this method is different from the iter used everywhere else, and is useless
        # once this method returns. Instead, create a TreeRowReference and work backwards
        # from that using paths any time we need to reference the store.
        self._repo_checks[repo.repo_id] = \
            RepoChecks(InputCheckHandler.add_check(self,
                                                   repo.repo_id,
                                                   self._check_repo_name,
                                                   Gtk.TreeRowReference.new(model, path)),
                       InputCheckHandler.add_check(self,
                                                   repo.repo_id,
                                                   self._check_repo_url,
                                                   Gtk.TreeRowReference.new(model, path)),
                       InputCheckHandler.add_check(self,
                                                   repo.repo_id,
                                                   self._check_repo_proxy,
                                                   Gtk.TreeRowReference.new(model, path)))

```

## ！ 此处忽略了一个重要的问题，就是在appsteam源更新后，需要确认软件选择，而在此时如果kernel可以正常处理，则不会有该问题

    但是代码的分析，还是得分析分析，毕竟已经分析到这了，起码找到该部分是如何触发重新加载源的，也是一个必要的过程
    往后可能还会和这块打交道，双内核选择原本该出现的位置就该在此页面上


    ！# 此处有较大的认知误区，installation_source.py 该spoke只要点进去就会被更新，
    而且之前所认为的在某些条件更改后才更新，也是在此错误的基础上推到出来的结论

    所以点进去，退出就会触发源的更新，此部分代码如何实现的，在哪实现的？

## 在appstream 在页面上状态发生改变后，源是会因其二更新的

``` python
    def apply(self):
        # 源更新状态检测
        source_changed = self._update_payload_source()
        # 仓库更新状态检测
        repo_changed = self._update_payload_repos()

        if source_changed or repo_changed or self._error:
            payloadMgr.restart_thread(self.payload, checkmount=False)
        else:
            log.debug("Nothing has changed - skipping payload restart.")

        self.clear_info()

   def _update_payload_repos(self):
        """ Change the payload repos to match the new edits

            This will add new repos to the addon repo list, remove
            ones that were removed and update any changes made to
            existing ones.

            :returns: True if any repo was changed, added or removed
            :rtype: bool
        """
        REPO_ATTRS = ("name", "baseurl", "mirrorlist", "metalink", "proxy", "enabled")
        changed = False

        with self._repo_store_lock:
            ui_orig_names = [r[REPO_OBJ].orig_name for r in self._repo_store]

            # Remove repos from payload that were removed in the UI
            # 根据不在源数据里仓库的名字，移除已经payload的仓库，此处维持着微弱的平衡
            # 如果该过程被修改，则可能引发位置的错误
            for repo_name in [r for r in self.payload.addons if r not in ui_orig_names]:
                repo = self.payload.get_addon_repo(repo_name)
                # TODO: Need an API to do this w/o touching dnf (not add_repo)
                # FIXME: Is this still needed for dnf?
                self.payload.data.repo.dataList().remove(repo)
                # 返回True 则证明仓库已更新，在source 中任何一个条件被更改，都在apply会触发更新的源的操作
                changed = True

            addon_repos = [(r[REPO_OBJ], self.payload.get_addon_repo(r[REPO_OBJ].orig_name))
                           for r in self._repo_store]
            # 如果勾选组建中存在，但是源中没有，则该源会被添加到payload 列表中
            for repo, orig_repo in addon_repos:
                if not orig_repo:
                    # TODO: Need an API to do this w/o touching dnf (not add_repo)
                    # FIXME: Is this still needed for dnf?
                    self.payload.data.repo.dataList().append(repo)
                    changed = True
                elif not cmp_obj_attrs(orig_repo, repo, REPO_ATTRS):
                    for attr in REPO_ATTRS:
                        setattr(orig_repo, attr, getattr(repo, attr))
                    changed = True
        # 以上条件都未检查出，则证明源未更新
        return changed

```
