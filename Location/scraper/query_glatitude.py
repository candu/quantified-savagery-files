import sys
import gflags
import glatitude
import httplib2

FLAGS = gflags.FLAGS
gflags.DEFINE_string('key', None, 'OAuth client ID')
gflags.DEFINE_string('secret', None, 'OAuth secret')
gflags.DEFINE_string('url', None, 'API URL')
gflags.MarkFlagAsRequired('key')
gflags.MarkFlagAsRequired('secret')
gflags.MarkFlagAsRequired('url')
try:
  sys.argv = FLAGS(sys.argv)
except gflags.FlagsError, e:
  print '''\
%s

Usage: %s ARGS
%s''' % (e, sys.argv[0], FLAGS)
  sys.exit(1)

credentials = glatitude.auth(FLAGS.key, FLAGS.secret)
http = httplib2.Http()
credentials.authorize(http)
resp, content = http.request(FLAGS.url)
print content
