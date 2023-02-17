# software_selection.py 分析(tui)

https://pms.uniontech.com/bug-view-184583.html
该 bug 主要问题为 默认的软件选择在某些情况下，不会被选择；
被选择的情况下，不会显示出来

问题分析：
默认选择不会显示出来，可以很容易的才想到是由于双内核添加到
软件选择中，导致软件列表显示具体更新的问题，但是具体的情况
还需分析代码，查看具体的执行过程

但是默认软件组不会被选择的情况，则暂时无思路

## 代码分析

``` python
# 该文件仅存在一个SoftwareSpoke类，继承自NormalTUISpoke
class SoftwareSpoke(NormalTUISpoke):

# from pyanaconda.ui.categories.software import SoftwareCategory
# 该变量是定义显示的目录，与gui类似，用于分组使用
category = SoftwareCategory

    # 初始化函数，使用传入参数做对象构造，初始化变量赋值(如果直接使用做右值会报错)
    def __init__(self, data, storage, payload):
        # 使用父类初始化函数（构造函数）完成对象构建
        super().__init__(data, storage, payload)
        self.title = N_("Software selection")
        self._container = None
        self.errors = []
        self._tx_id = None
        # 已选择的环境
        self._selected_environment = None
        # 当前环境
        self.environment = None
        self._addons_selection = set()
        self.addons = set()

        self._orig_kernel = None

        # 等待payload 进程加载完毕，self.data.repo.dataList()才能读取到数据
        # 不然该列表可能是空的
        threadMgr.wait(THREAD_PAYLOAD)
        self._kernel_repos = []
        if arch.is_loongarch():
            self._kernel_repos = ['kernel419']
        else:
            for repo in self.data.repo.dataList():
                if "kernel" in repo.name:
                    self._kernel_repos.append(repo.name)

        # 初始化环境和组件置空，方便检测改变
        self._orig_env = None
        self._orig_addons = set()

        self._kickstarted = flags.automatedInstall and self.data.packages.seen

        # 注册payload监听事件，包含payload 启动，完成，报错三个状态的监听和其对应的回掉函数
        # !start 中，置空已选择的环境为None，对此bug有较大的影响，在注释后可以正常达到预期
        # 目前经过反复测试，只有修改此处可以正常，其他地方的修改，均会导致更严重的问题

        payloadMgr.add_listener(PayloadState.STARTED, self._payload_start)
        payloadMgr.add_listener(PayloadState.FINISHED, self._payload_finished)
        payloadMgr.add_listener(PayloadState.ERROR, self._payload_error)

    def _payload_start(self):
        # Source is changing, invalidate the software selection and clear the
        # errors

        # 此处为最终的修改，单独以XXX标记，如果以后有更好的修改方法，此处必须修改！！
        # 此处情况 _selected_environment 已选择的环境是必要的操作
        # 但是kernel加载会导致,payload 重新执行，清空已选择的列表
        # 显示使用的是该列表，所以导致bug 所描述的问题，目前注释改情况已选列表
        # 经过多次测试不会导致其他问题

        # XXX: This comment fix bug#184583,but it isn't the best way
        # self._selected_environment = None
        self._addons_selection = set()
        self.errors = []

    def _payload_finished(self):
        
        self.environment = self.data.packages.environment
        self.addons = self._get_selected_addons()
        self._orig_env = None
        self._orig_addons = None
        log.debug("Payload restarted, set new info and clear the old one.")

    def _payload_error(self):
        self.errors = [payloadMgr.error]

    def initialize(self):
        # Start a thread to wait for the payload and run the first, automatic
        # dependency check
        self.initialize_start()
        super().initialize()
        # 添加进程检测和目标初始化函数
        threadMgr.add(AnacondaThread(name=THREAD_SOFTWARE_WATCHER,
                                     target=self._initialize))

    def _initialize(self):
        threadMgr.wait(THREAD_PAYLOAD)

        if not self.current_kernel:
            if len(self._kernel_repos) > 0:
                self.current_kernel = list(self._kernel_repos)[0]

        if not self._kickstarted:
            # If an environment was specified in the configuration, use that.
            # Otherwise, select the first environment.
            if self.payload.environments:
                # 从comps 文件中获取环境列表
                environments = self.payload.environments

                # conf.payload.default_environment 配置文件中
                # 目前为/etc/anaconda/product.d/Uniontech.conf
                # 由SOURCE直接写入到目录，而A版原本的uos.conf 被exclude
                if conf.payload.default_environment in environments:
                    # 从配置中读取默认加载环境
                    self._selected_environment = conf.payload.default_environment
                else:
                    # 从环境列表中选取第一项为默认环境,但第一个环境不一定是graphical-server-environment
                    self._selected_environment = environments[0]
                # !此处最后在[payload]中配置了default_environment = graphical-server-environment

        # Apply the initial selection
        # 在最终显示列表，先加载kernel选项
        self.check_kernel_selection()
        # 再加载其余的选项
        self._apply()
        # 上述选项，两个调换后kernel 可以后加载，经过测试，并非kernel先加载导致的显示问题

        # Wait for the software selection thread that might be started by _apply().
        # We are already running in a thread, so it should not needlessly block anything
        # and only like this we can be sure we are really initialized.
        threadMgr.wait(THREAD_CHECK_SOFTWARE)

        # report that the software spoke has been initialized
        # 在initialize中，控制器获取后，有执行start操作，此处调用层级不同，且跨度有点大
        self.initialize_done()
    
    # 判断内核是否改变过，返回判断结果,用于更新kernel源
    @property
    def changed_kernel(self):
        if self.current_kernel == self._orig_kernel:
            return False
        else:
            return True
    
    # 上述是否可以优化成以下写法？
    #@property
    #def changed_kernel(self):
    #    return self.current_kernel != self._orig_kernel

    # 转换环境名称为对应环境的id
    def _translate_env_name_to_id(self, environment):
        """ Return the id of the selected environment or None. """
        if environment is None:
            # None means environment is not set, no need to try translate that to an id
            return None
        try:
            return self.payload.environment_id(environment)
        except NoSuchGroup:
            return None
    
    # 以id获取对应环境,所有组件
    def _get_available_addons(self, environment_id):
        """ Return all add-ons of the specific environment. """
        addons = []

        if environment_id in self.payload.environment_addons:
            for addons_list in self.payload.environment_addons[environment_id]:
                addons.extend(addons_list)

        return addons

    # 获取已选择的组件
    def _get_selected_addons(self):
        """ Return selected add-ons. """
        return {group.name for group in self.payload.data.packages.groupList}

    # tui/hub/__init__.py 调用
    # 如果返回False,则对应spoke 不可见,在gui上不可见的spoke 可以被删除，也将会被删除
    # 在tui 上，如果返回True 则，spoke 将会被初始化
    @property
    def showable(self):
        #？此处的判断条件不能理解，以前也没注意到过
        return self.payload.type == PAYLOAD_TYPE_DNF

    #？此函数未使用过，是否多余
    @property
    def showable_kernel(self):
        return isinstance(self.payload, Payload)

# 返回软件选择spoke 状态，显示在主界面上
@property
    def status(self):
        """ Where we are in the process """
        if self.errors:
            return _("Error checking software selection")
        if not self.ready:
            return _("Processing...")
        if not self.payload.base_repo:
            return _("Installation source not set up")
        if not self.txid_valid:
            return _("Source changed - please verify")

        #!如果环境为空，则返回"Nothing selected"，该提示信息
        #!!!需要着重关注对此变量赋值的过程，可能可以研究清楚双内核加入导致的进程问题
        if not self.environment:
            # KS installs with %packages will have an env selected, unless
            # they did an install without a desktop environment. This should
            # catch that one case.
            if self._kickstarted:
                return _("Custom software selected")
            return _("Nothing selected")

        return self.payload.environment_description(self.environment)[0]
        
        #!!!此处添加的信息永远也不会执行到
        if self._error_msgs:
            return _("Error select kernel")
        return self.current_kernel

    @property
    def completed(self):
        """ Make sure our threads are done running and vars are set.

           WARNING: This can be called before the spoke is finished initializing
           if the spoke starts a thread. It should make sure it doesn't access
           things until they are completely setup.
        """
        # spoke 状态ready，通过hubQ可以控制，或直接执行ready 函数；无报错 tx_id 匹配 payload的 作用未知
        processing_done = self.ready and not self.errors and self.txid_valid

        # 上述经常状态为True base_repo 加载成功
        if flags.automatedInstall or self._kickstarted:
            # 自动安装或ks 安装，软件包seens?已选择软件列表在ks文件中
            return processing_done and self.payload.base_repo and self.data.packages.seen
        else:
            # 选择的安装环境不为空
            return processing_done and self.payload.base_repo and self.environment is not None

    #?tx id 是什么 
    @property
    def txid_valid(self):
        """ Whether we have a valid dnf tx id. """
        return self._tx_id == self.payload.tx_id

    def refresh(self, args=None):
        """ Refresh screen. """
        NormalTUISpoke.refresh(self, args)

        threadMgr.wait(THREAD_PAYLOAD)
        self._container = None

        if not self.payload.base_repo:
            message = TextWidget(_("Installation source needs to be set up first."))
            self.window.add_with_separator(message)
            return

        threadMgr.wait(THREAD_CHECK_SOFTWARE)
        self._container = ListColumnContainer(2, columns_width=38, spacing=2)

        if args is None:
            msg = self._refresh_kernels()
            msg = self._refresh_environments()
        else:
            msg = self._refresh_addons(args)

        self.window.add_with_separator(TextWidget(msg))
        self.window.add_with_separator(self._container)

    # 更新kernel 选项
    def _refresh_kernels(self):
        kernel_keys =self._kernel_repos
        for kernel in kernel_keys:
            selected = (self.current_kernel == kernel)
            if kernel == 'kernel419':
                kernel_desc = _("ANCK")
                kernel_info = _("Support UOS verified platform")
            elif kernel == 'kernel510':
                kernel_desc = _("RHCK")
                kernel_info = _("Technology Previews")
            else:
                kernel_desc = ''
                kernel_info = ''
            widget = CheckboxWidget(title=kernel, completed=selected)
            self._container.add(widget, callback=self._set_kernel_callback, data=kernel)
        return _("Kernel List")

    def _refresh_environments(self):
        environments = self.payload.environments

        for env in environments:
            name = self.payload.environment_description(env)[0]
            selected = (env == self._selected_environment)
            widget = CheckboxWidget(title="%s" % name, completed=selected)
            self._container.add(widget, callback=self._set_environment_callback, data=env)

        return _("Base environment")

    def _refresh_addons(self, available_addons):
        for addon_id in available_addons:
            name = self.payload.group_description(addon_id)[0]
            selected = addon_id in self._addons_selection
            widget = CheckboxWidget(title="%s" % name, completed=selected)
            self._container.add(widget, callback=self._set_addons_callback, data=addon_id)

        if available_addons:
            return _("Additional software for selected environment")
        else:
            return _("No additional software to select.")

    def _set_kernel_callback(self, data):
        self.current_kernel = data

    def _set_environment_callback(self, data):
        self._selected_environment = data

    def _set_addons_callback(self, data):
        addon = data
        if addon not in self._addons_selection:
            self._addons_selection.add(addon)
        else:
            self._addons_selection.remove(addon)

    def input(self, args, key):
        """ Handle the input; this chooses the desktop environment. """
        if self._container is not None and self._container.process_user_input(key):
            self.redraw()
        else:
            # TRANSLATORS: 'c' to continue
            if key.lower() == C_('TUI|Spoke Navigation', 'c'):
                threadMgr.wait(THREAD_PAYLOAD)

                # No environment was selected, close
                if self._selected_environment is None:
                    self.close()

                # The environment was selected, switch screen
                elif args is None:
                    # Get addons for the selected environment
                    environment = self._selected_environment
                    environment_id = self._translate_env_name_to_id(environment)
                    addons = self._get_available_addons(environment_id)

                    # Switch the screen
                    ScreenHandler.replace_screen(self, addons)

                # The addons were selected, apply and close
                else:
                    self.apply()
                    self.close()
            else:
                return super().input(args, key)

        return InputState.PROCESSED

    @property
    def ready(self):
        """ If we're ready to move on. """
        return (not threadMgr.get(THREAD_PAYLOAD) and
                not threadMgr.get(THREAD_CHECK_SOFTWARE) and
                not threadMgr.get(THREAD_SOFTWARE_WATCHER))

    @property
    def current_kernel(self):
        return self.payload.current_kernel

    @current_kernel.setter
    def current_kernel(self, value):
        self.payload.current_kernel = value

    def apply(self):
        """ Apply our selections """
        # no longer using values from kickstart
        self._kickstarted = False
        self.data.packages.seen = True
        # _apply depends on a value of _kickstarted
        self.check_kernel_selection()
        self._apply()

    def _apply(self):
        """ Private apply. """
        self.environment = self._selected_environment
        self.addons = self._addons_selection if self.environment is not None else set()

        log.debug("Apply called old env %s, new env %s and addons %s",
                  self._orig_env, self.environment, self.addons)

        if self.environment is None:
            return

        changed = False

        # Not a kickstart with packages, setup the selected environment and addons
        if not self._kickstarted:

            # Changed the environment or addons, clear and setup
            if not self._orig_env \
                    or self._orig_env != self.environment \
                    or set(self._orig_addons) != set(self.addons):

                log.debug("Setting new software selection old env %s, new env %s and addons %s",
                          self._orig_env, self.environment, self.addons)

                self.payload.data.packages.packageList = []
                self.data.packages.groupList = []
                self.payload.select_environment(self.environment)

                environment_id = self._translate_env_name_to_id(self.environment)
                available_addons = self._get_available_addons(environment_id)

                for addon_id in available_addons:
                    if addon_id in self.addons:
                        self.payload.select_group(addon_id)

                changed = True

            self._orig_env = self.environment
            self._orig_addons = set(self.addons)

        # Check the software selection
        if changed or self._kickstarted:
            threadMgr.add(AnacondaThread(name=THREAD_CHECK_SOFTWARE,
                                         target=self.check_software_selection))

    # 重新加载kernel源，如果kernel源做了改变的话
    def check_kernel_selection(self):
       # we do this only kernel changed
        threadMgr.wait(THREAD_PAYLOAD)
        if self.changed_kernel:
            if os.path.exists("/tmp/.anaconda_payload_finished"):
                os.remove("/tmp/.anaconda_payload_finished")
            self._repos_backup = copy.copy(self.data.repo.dataList())
            for r in self._repos_backup:
                if r.name in self._kernel_repos:
                    self.payload.data.repo.dataList().remove(r)
                    if r.name == self.current_kernel:
                        r.enabled = True
                    else:
                        r.enabled = False
                    self.payload.data.repo.dataList().append(r)

            #if self._orig_kernel is not None:
            payloadMgr.restart_thread(self.payload, checkmount=False)

            self._orig_kernel = self.current_kernel
            threadMgr.wait(THREAD_PAYLOAD)
            threadMgr.wait(THREAD_CHECK_SOFTWARE)

    def check_software_selection(self):
        while not os.path.exists("/tmp/.anaconda_payload_finished"):
            log.debug("check_software_selection: wait payload finished...")
            sleep(3)
        """ Depsolving """
        try:
            self.payload.check_software_selection()
        except DependencyError as e:
            self.errors = [str(e)]
            self._tx_id = None
            log.warning("Transaction error %s", str(e))
        else:
            self._tx_id = self.payload.tx_id
```