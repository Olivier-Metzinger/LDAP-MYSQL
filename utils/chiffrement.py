def roederer_user_token_encrypt(data, parameters):
	key = 'key'
	iv = 'iv'
	pwd = data['uuid'].data['timestamp']
	method = "AES-256-CBC"
	// encode

	$hashedPwd = hash('sha512', $pwd);
	$ser = base64_encode(serialize($data));

	$cipher = openssl_encrypt($ser, $method, $key, true, $iv);
	$bcipher = urlencode(base64_encode($cipher));

	return 'pwd=' . $hashedPwd . '&token=' . $bcipher;
}

function token_decrypt($pwd, $token) {
	$key = 'key';
	$iv = 'iv';
	$method = 'AES-256-CBC';
	$cipher = base64_decode(urldecode($token));
	$serialized = openssl_decrypt($cipher, $method, $key, true, $iv);
	$userData = unserialize(base64_decode($serialized));

	$h2 = hash('sha512', $userData['uuid'].$userData['timestamp']);
	$res = $pwd == $h2;

	return array('auth' => $res, 'userData' => $userData);
}

//$data = array();
//$data['uuid'] = 123;
//$data['timestamp'] = 1555401475;
//$data['password'] = "coucou";
//$url = roed_user_token_encrypt($data);
//echo $url;


$url = "pwd=url&token=%%2F3k2LhidPw%3D%3D";

$array = explode("&", $url);
$pwd = explode("=", $array[0])[1];
$token = explode("=", $array[1])[1];
var_dump($pwd);
var_dump($token);
$return = token_decrypt($pwd, $token);

var_dump($return);
?>
