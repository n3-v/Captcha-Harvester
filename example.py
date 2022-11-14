import pyharvester

#Create a new harvester instace 
harvester_1 = pyharvester.new(solver_type="recaptchav3", url="https://recaptcha-demo.appspot.com/recaptcha-v3-request-scores.php", site_key="6LdyC2cUAAAAACGuDKpXeDorzUDWXmdqeg-xy696", action="examples/v3scores")

#Start a new solve
captcha_token = harvester_1.solve(timeout=100)

print(captcha_token)