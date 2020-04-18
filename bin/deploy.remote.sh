ACCOUNT=tgrayson
ENV_VARS="-e HOST=https://raw.githubusercontent.com"

declare -A hostports
hostports[pointillism]=5001
hostports[cribnot.es]=5000

export ADMIN_USER=admin@ipsumllc.com 
export ADMIN_PASS=tugboat 
export LDAP_HOST=ipsumllc.com 
export PAYPAL_CLIENT_ID=AbGIpC8ukqd4cb744uNxvjvwS0-ET3U39gpONKAN2d7IBTwrCjBTZ2l7B8R2yr1SPepqasUUYCX4u1Sq
export GITHUB_SECRET=b1988c869bcd64271843c463bc9aec61ecfa4db5 
export GITHUB_CLIENT_ID=Iv1.216e3a2bbb5daf1f 
export PROJECT=pointillism

docker pull $ACCOUNT/$PROJECT:latest
docker RENAME $PROJECT $PROJECT.last
docker stop $PROJECT.last
sudo docker run --name $PROJECT -e ADMIN_USER=admin@ipsumllc.com -e ADMIN_PASS=tugboat -e LDAP_HOST=ipsumllc.com -e GITHUB_SECRET=b1988c869bcd64271843c463bc9aec61ecfa4db5 -e GITHUB_CLIENT_ID=Iv1.216e3a2bbb5daf1f -e PAYPAL_CLIENT_ID=AbGIpC8ukqd4cb744uNxvjvwS0-ET3U39gpONKAN2d7IBTwrCjBTZ2l7B8R2yr1SPepqasUUYCX4u1Sq -d -p 5001:5001 --restart=always tgrayson/$PROJECT:latest
docker rm $PROJECT.last
docker images prune
