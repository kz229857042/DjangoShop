from rest_framework.renderers import JSONRenderer


class CustomRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        '''
        :param data: 返回的数据
        :param accepted_media_type: 接收的类型
        :param renderer_context: 呈现的内容
        :return:
        '''
        # 如果有请求的数据过来  类似于 if request.method == 'POST'
        if renderer_context:
            # 如果数据格式为字典格式
            if isinstance(data, dict):
                # 获取字典格式中的msg参数
                msg = data.pop('msg', '请求成功')
                # 获取字典格式当中的code参数
                code = data.pop('code', 0)
            # 如果不是字典格式
            else:
                msg = '请求成功'
                code = 0
            # 重新构造数据格式
            ret = {
                'msg': msg,
                'code': code,
                'author': '哈哈',
                'data': data
            }
            return super().render(ret, accepted_media_type, renderer_context)  # 返回数据格式
        else:
            return super().render(data, accepted_media_type, renderer_context)  # 如果没有发生修改，则返回原格式
