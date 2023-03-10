# python

菜鸟教程 os pipe
https://www.runoob.com/python/os-pipe.html
https://blog.csdn.net/qq_42730750/article/details/127729762
python 管道通信

https://www.runoob.com/w3cnote/python3-subprocess.html
子进程

## _posixsubprocess

该对象在最新的版本中已经被取代了

https://vimsky.com/examples/detail/python-method-_posixsubprocess.fork_exec.html


Python _posixsubprocess.fork_exec方法代码示例

本文整理汇总了Python中_posixsubprocess.fork_exec方法的典型用法代码示例。如果您正苦于以下问题：Python _posixsubprocess.fork_exec方法的具体用法？Python _posixsubprocess.fork_exec怎么用？Python _posixsubprocess.fork_exec使用的例子？那么恭喜您, 这里精选的方法代码示例或许可以为您提供帮助。您也可以进一步了解该方法所在类_posixsubprocess的用法示例。

在下文中一共展示了_posixsubprocess.fork_exec方法的15个代码示例，这些例子默认根据受欢迎程度排序。您可以为喜欢或者感觉有用的代码点赞，您的评价将有助于我们的系统推荐出更棒的Python代码示例。
示例1: create_fork_exec

# 需要导入模块: import _posixsubprocess [as 别名]
# 或者: from _posixsubprocess import fork_exec [as 别名]
def create_fork_exec(original_name):
    """
    _posixsubprocess.fork_exec(args, executable_list, close_fds, ... (13 more))
    """

    def new_fork_exec(args, *other_args):
        import _posixsubprocess  # @UnresolvedImport
        if _get_apply_arg_patching():
            args = patch_args(args)
            send_process_created_message()

        return getattr(_posixsubprocess, original_name)(args, *other_args)

    return new_fork_exec 

开发者ID:fabioz，项目名称:PyDev.Debugger，代码行数:16，代码来源:pydev_monkey.py

示例2: create_warn_fork_exec

# 需要导入模块: import _posixsubprocess [as 别名]
# 或者: from _posixsubprocess import fork_exec [as 别名]
def create_warn_fork_exec(original_name):
    """
    _posixsubprocess.fork_exec(args, executable_list, close_fds, ... (13 more))
    """

    def new_warn_fork_exec(*args):
        try:
            import _posixsubprocess
            warn_multiproc()
            return getattr(_posixsubprocess, original_name)(*args)
        except:
            pass

    return new_warn_fork_exec 

开发者ID:fabioz，项目名称:PyDev.Debugger，代码行数:16，代码来源:pydev_monkey.py

示例3: patch_new_process_functions_with_warning

# 需要导入模块: import _posixsubprocess [as 别名]
# 或者: from _posixsubprocess import fork_exec [as 别名]
def patch_new_process_functions_with_warning():
    monkey_patch_os('execl', create_warn_multiproc)
    monkey_patch_os('execle', create_warn_multiproc)
    monkey_patch_os('execlp', create_warn_multiproc)
    monkey_patch_os('execlpe', create_warn_multiproc)
    monkey_patch_os('execv', create_warn_multiproc)
    monkey_patch_os('execve', create_warn_multiproc)
    monkey_patch_os('execvp', create_warn_multiproc)
    monkey_patch_os('execvpe', create_warn_multiproc)
    monkey_patch_os('spawnl', create_warn_multiproc)
    monkey_patch_os('spawnle', create_warn_multiproc)
    monkey_patch_os('spawnlp', create_warn_multiproc)
    monkey_patch_os('spawnlpe', create_warn_multiproc)
    monkey_patch_os('spawnv', create_warn_multiproc)
    monkey_patch_os('spawnve', create_warn_multiproc)
    monkey_patch_os('spawnvp', create_warn_multiproc)
    monkey_patch_os('spawnvpe', create_warn_multiproc)
    monkey_patch_os('posix_spawn', create_warn_multiproc)

    if not IS_JYTHON:
        if not IS_WINDOWS:
            monkey_patch_os('fork', create_warn_multiproc)
            try:
                import _posixsubprocess
                monkey_patch_module(_posixsubprocess, 'fork_exec', create_warn_fork_exec)
            except ImportError:
                pass
        else:
            # Windows
            try:
                import _subprocess
            except ImportError:
                import _winapi as _subprocess
            monkey_patch_module(_subprocess, 'CreateProcess', create_CreateProcessWarnMultiproc) 

开发者ID:fabioz，项目名称:PyDev.Debugger，代码行数:36，代码来源:pydev_monkey.py

示例4: test_fork_exec

# 需要导入模块: import _posixsubprocess [as 别名]
# 或者: from _posixsubprocess import fork_exec [as 别名]
def test_fork_exec(self):
        # Issue #22290: fork_exec() must not crash on memory allocation failure
        # or other errors
        import _posixsubprocess
        gc_enabled = gc.isenabled()
        try:
            # Use a preexec function and enable the garbage collector
            # to force fork_exec() to re-enable the garbage collector
            # on error.
            func = lambda: None
            gc.enable()

            for args, exe_list, cwd, env_list in (
                (123,      [b"exe"], None, [b"env"]),
                ([b"arg"], 123,      None, [b"env"]),
                ([b"arg"], [b"exe"], 123,  [b"env"]),
                ([b"arg"], [b"exe"], None, 123),
            ):
                with self.assertRaises(TypeError):
                    _posixsubprocess.fork_exec(
                        args, exe_list,
                        True, [], cwd, env_list,
                        -1, -1, -1, -1,
                        1, 2, 3, 4,
                        True, True, func)
        finally:
            if not gc_enabled:
                gc.disable() 

开发者ID:Microvellum，项目名称:Fluid-Designer，代码行数:30，代码来源:test_subprocess.py

示例5: test_fork_exec_sorted_fd_sanity_check

# 需要导入模块: import _posixsubprocess [as 别名]
# 或者: from _posixsubprocess import fork_exec [as 别名]
def test_fork_exec_sorted_fd_sanity_check(self):
        # Issue #23564: sanity check the fork_exec() fds_to_keep sanity check.
        import _posixsubprocess
        gc_enabled = gc.isenabled()
        try:
            gc.enable()

            for fds_to_keep in (
                (-1, 2, 3, 4, 5),  # Negative number.
                ('str', 4),  # Not an int.
                (18, 23, 42, 2**63),  # Out of range.
                (5, 4),  # Not sorted.
                (6, 7, 7, 8),  # Duplicate.
            ):
                with self.assertRaises(
                        ValueError,
                        msg='fds_to_keep={}'.format(fds_to_keep)) as c:
                    _posixsubprocess.fork_exec(
                        [b"false"], [b"false"],
                        True, fds_to_keep, None, [b"env"],
                        -1, -1, -1, -1,
                        1, 2, 3, 4,
                        True, True, None)
                self.assertIn('fds_to_keep', str(c.exception))
        finally:
            if not gc_enabled:
                gc.disable() 

开发者ID:Microvellum，项目名称:Fluid-Designer，代码行数:29，代码来源:test_subprocess.py

示例6: test_seq_bytes_to_charp_array

# 需要导入模块: import _posixsubprocess [as 别名]
# 或者: from _posixsubprocess import fork_exec [as 别名]
def test_seq_bytes_to_charp_array(self):
        # Issue #15732: crash in _PySequence_BytesToCharpArray()
        class Z(object):
            def __len__(self):
                return 1
        self.assertRaises(TypeError, _posixsubprocess.fork_exec,
                          1,Z(),3,[1, 2],5,6,7,8,9,10,11,12,13,14,15,16,17)
        # Issue #15736: overflow in _PySequence_BytesToCharpArray()
        class Z(object):
            def __len__(self):
                return sys.maxsize
            def __getitem__(self, i):
                return b'x'
        self.assertRaises(MemoryError, _posixsubprocess.fork_exec,
                          1,Z(),3,[1, 2],5,6,7,8,9,10,11,12,13,14,15,16,17) 

开发者ID:Microvellum，项目名称:Fluid-Designer，代码行数:17，代码来源:test_capi.py

示例7: test_subprocess_fork_exec

# 需要导入模块: import _posixsubprocess [as 别名]
# 或者: from _posixsubprocess import fork_exec [as 别名]
def test_subprocess_fork_exec(self):
        class Z(object):
            def __len__(self):
                return 1

        # Issue #15738: crash in subprocess_fork_exec()
        self.assertRaises(TypeError, _posixsubprocess.fork_exec,
                          Z(),[b'1'],3,[1, 2],5,6,7,8,9,10,11,12,13,14,15,16,17) 

开发者ID:Microvellum，项目名称:Fluid-Designer，代码行数:10，代码来源:test_capi.py

示例8: spawnv_passfds

# 需要导入模块: import _posixsubprocess [as 别名]
# 或者: from _posixsubprocess import fork_exec [as 别名]
def spawnv_passfds(path, args, passfds):
    import _posixsubprocess
    passfds = sorted(passfds)
    errpipe_read, errpipe_write = os.pipe()
    try:
        return _posixsubprocess.fork_exec(
            args, [os.fsencode(path)], True, passfds, None, None,
            -1, -1, -1, -1, -1, -1, errpipe_read, errpipe_write,
            False, False, None)
    finally:
        os.close(errpipe_read)
        os.close(errpipe_write) 

开发者ID:Microvellum，项目名称:Fluid-Designer，代码行数:14，代码来源:util.py

示例9: spawnv_passfds

# 需要导入模块: import _posixsubprocess [as 别名]
# 或者: from _posixsubprocess import fork_exec [as 别名]
def spawnv_passfds(path, args, passfds):
    import _posixsubprocess
    passfds = tuple(sorted(map(int, passfds)))
    errpipe_read, errpipe_write = os.pipe()
    try:
        return _posixsubprocess.fork_exec(
            args, [os.fsencode(path)], True, passfds, None, None,
            -1, -1, -1, -1, -1, -1, errpipe_read, errpipe_write,
            False, False, None)
    finally:
        os.close(errpipe_read)
        os.close(errpipe_write) 

开发者ID:CedricGuillemet，项目名称:Imogen，代码行数:14，代码来源:util.py

示例10: test_fork_exec

# 需要导入模块: import _posixsubprocess [as 别名]
# 或者: from _posixsubprocess import fork_exec [as 别名]
def test_fork_exec(self):
        # Issue #22290: fork_exec() must not crash on memory allocation failure
        # or other errors
        import _posixsubprocess
        gc_enabled = gc.isenabled()
        try:
            # Use a preexec function and enable the garbage collector
            # to force fork_exec() to re-enable the garbage collector
            # on error.
            func = lambda: None
            gc.enable()

            executable_list = "exec"   # error: must be a sequence

            for args, exe_list, cwd, env_list in (
                (123,      [b"exe"], None, [b"env"]),
                ([b"arg"], 123,      None, [b"env"]),
                ([b"arg"], [b"exe"], 123,  [b"env"]),
                ([b"arg"], [b"exe"], None, 123),
            ):
                with self.assertRaises(TypeError):
                    _posixsubprocess.fork_exec(
                        args, exe_list,
                        True, [], cwd, env_list,
                        -1, -1, -1, -1,
                        1, 2, 3, 4,
                        True, True, func)
        finally:
            if not gc_enabled:
                gc.disable() 

开发者ID:IronLanguages，项目名称:ironpython3，代码行数:32，代码来源:test_subprocess.py

示例11: test_fork_exec

# 需要导入模块: import _posixsubprocess [as 别名]
# 或者: from _posixsubprocess import fork_exec [as 别名]
def test_fork_exec(self):
        # Issue #22290: fork_exec() must not crash on memory allocation failure
        # or other errors
        import _posixsubprocess
        gc_enabled = gc.isenabled()
        try:
            # Use a preexec function and enable the garbage collector
            # to force fork_exec() to re-enable the garbage collector
            # on error.
            func = lambda: None
            gc.enable()

            for args, exe_list, cwd, env_list in (
                (123,      [b"exe"], None, [b"env"]),
                ([b"arg"], 123,      None, [b"env"]),
                ([b"arg"], [b"exe"], 123,  [b"env"]),
                ([b"arg"], [b"exe"], None, 123),
            ):
                with self.assertRaises(TypeError):
                    _posixsubprocess.fork_exec(
                        args, exe_list,
                        True, (), cwd, env_list,
                        -1, -1, -1, -1,
                        1, 2, 3, 4,
                        True, True, func)
        finally:
            if not gc_enabled:
                gc.disable() 

开发者ID:ShikyoKira，项目名称:Project-New-Reign---Nemesis-Main，代码行数:30，代码来源:test_subprocess.py

示例12: test_fork_exec_sorted_fd_sanity_check

# 需要导入模块: import _posixsubprocess [as 别名]
# 或者: from _posixsubprocess import fork_exec [as 别名]
def test_fork_exec_sorted_fd_sanity_check(self):
        # Issue #23564: sanity check the fork_exec() fds_to_keep sanity check.
        import _posixsubprocess
        class BadInt:
            first = True
            def __init__(self, value):
                self.value = value
            def __int__(self):
                if self.first:
                    self.first = False
                    return self.value
                raise ValueError

        gc_enabled = gc.isenabled()
        try:
            gc.enable()

            for fds_to_keep in (
                (-1, 2, 3, 4, 5),  # Negative number.
                ('str', 4),  # Not an int.
                (18, 23, 42, 2**63),  # Out of range.
                (5, 4),  # Not sorted.
                (6, 7, 7, 8),  # Duplicate.
                (BadInt(1), BadInt(2)),
            ):
                with self.assertRaises(
                        ValueError,
                        msg='fds_to_keep={}'.format(fds_to_keep)) as c:
                    _posixsubprocess.fork_exec(
                        [b"false"], [b"false"],
                        True, fds_to_keep, None, [b"env"],
                        -1, -1, -1, -1,
                        1, 2, 3, 4,
                        True, True, None)
                self.assertIn('fds_to_keep', str(c.exception))
        finally:
            if not gc_enabled:
                gc.disable() 

开发者ID:ShikyoKira，项目名称:Project-New-Reign---Nemesis-Main，代码行数:40，代码来源:test_subprocess.py

示例13: test_seq_bytes_to_charp_array

# 需要导入模块: import _posixsubprocess [as 别名]
# 或者: from _posixsubprocess import fork_exec [as 别名]
def test_seq_bytes_to_charp_array(self):
        # Issue #15732: crash in _PySequence_BytesToCharpArray()
        class Z(object):
            def __len__(self):
                return 1
        self.assertRaises(TypeError, _posixsubprocess.fork_exec,
                          1,Z(),3,(1, 2),5,6,7,8,9,10,11,12,13,14,15,16,17)
        # Issue #15736: overflow in _PySequence_BytesToCharpArray()
        class Z(object):
            def __len__(self):
                return sys.maxsize
            def __getitem__(self, i):
                return b'x'
        self.assertRaises(MemoryError, _posixsubprocess.fork_exec,
                          1,Z(),3,(1, 2),5,6,7,8,9,10,11,12,13,14,15,16,17) 

开发者ID:ShikyoKira，项目名称:Project-New-Reign---Nemesis-Main，代码行数:17，代码来源:test_capi.py

示例14: test_subprocess_fork_exec

# 需要导入模块: import _posixsubprocess [as 别名]
# 或者: from _posixsubprocess import fork_exec [as 别名]
def test_subprocess_fork_exec(self):
        class Z(object):
            def __len__(self):
                return 1

        # Issue #15738: crash in subprocess_fork_exec()
        self.assertRaises(TypeError, _posixsubprocess.fork_exec,
                          Z(),[b'1'],3,(1, 2),5,6,7,8,9,10,11,12,13,14,15,16,17) 

开发者ID:ShikyoKira，项目名称:Project-New-Reign---Nemesis-Main，代码行数:10，代码来源:test_capi.py

示例15: create_fork_exec

# 需要导入模块: import _posixsubprocess [as 别名]
# 或者: from _posixsubprocess import fork_exec [as 别名]
def create_fork_exec(original_name):
    """
    _posixsubprocess.fork_exec(args, executable_list, close_fds, ... (13 more))
    """
    def new_fork_exec(args, *other_args):
        import _posixsubprocess  # @UnresolvedImport
        args = patch_args(args)
        return getattr(_posixsubprocess, original_name)(args, *other_args)
    return new_fork_exec 

开发者ID:mrknow，项目名称:filmkodi，代码行数:11，代码来源:pydev_monkey.py


注：本文中的_posixsubprocess.fork_exec方法示例由纯净天空整理自Github/MSDocs等开源代码及文档管理平台，相关代码片段筛选自各路编程大神贡献的开源项目，源码版权归原作者所有，传播和使用请参考对应项目的License；未经允许，请勿转载。
