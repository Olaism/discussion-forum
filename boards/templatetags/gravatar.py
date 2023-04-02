import hashlib
from urllib.parse import urlencode
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

# return only the URL of the gravatar
# TEMPLATE USE:  {{ email|gravatar_url:150 }}


# @register.filter
# def gravatar_url(email, size=40):
#     default = "https://example.com/static/images/defaultavatar.jpg"
#     return "https://www.gravatar.com/avatar/%s?%s" % (hashlib.md5(email.lower()).hexdigest(), urllib.urlencode({'d': default, 's': str(size)}))

# # return an image tag with the gravatar
# # TEMPLATE USE:  {{ email|gravatar:150 }}


# @register.filter
# def gravatar(email, size=40):
#     url = gravatar_url(email, size)
#     return mark_safe('' % (url, size, size))


@register.filter
def gravatar(user):
    email = user.email.lower().encode("utf-8")
    default = "mm"
    size = 256
    url = "https://www.gravatar.com/avatar/{md5}?{params}".format(
        md5=hashlib.md5(email).hexdigest(),
        params=urlencode({"d": default, "s": str(size)}),
    )
    return url
