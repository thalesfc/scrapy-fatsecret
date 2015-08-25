import re


def get_user_id(response):
    return response.xpath('//div[@class="breadcrumb_link"][3]\
            /a/@title').extract()


def get_page_id(response):
    return re.search("id=(\d+)", response.url).group(1)

import warnings


def deprecated(func):
    '''This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emitted
    when the function is used.'''
    def new_func(*args, **kwargs):
        warnings.warn("Call to deprecated function {}.".format(func.__name__),
                      category=DeprecationWarning)
        return func(*args, **kwargs)
    new_func.__name__ = func.__name__
    new_func.__doc__ = func.__doc__
    new_func.__dict__.update(func.__dict__)
    return new_func
