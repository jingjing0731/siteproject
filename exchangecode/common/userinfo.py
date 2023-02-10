class UserInfo():
    def validate(self, token):
        """
        attrs['token']: 是请求的token
        settings.SECRET_KEY: setting.py默认的key 除非在配置文件中修改了
        algorithms: 加密的方法
        """
        decoded_data = jwt_decode(attrs['token'], settings.SECRET_KEY, algorithms=["HS256"])
        return decoded_data