def user_changed(sender, instance, **kwargs):
    #import 写在函数里避免循环依赖：
        # 如果写在外面，编译的时候：accounts/listeners 调用了accounts.services.UserService
        #                    UserService 调用了 UserProfile
        #                    UserProfile.py 里有调用了listeners--> 循环依赖，写在函数里可以避免编译时产生的循环依赖
        from accounts.services import UserService
        UserService.invalidate_user(instance.id)

def profile_changed(sender, instance, **kwargs):
    # import 写在函数里面避免循环依赖
    from accounts.services import UserService
    UserService.invalidate_profile(instance.user_id)


