
## Python Captcha Harvester

Simple captcha harvester for python. Currently supporting Hcapctha and Recaptcha (v2, v3)


## Install dependencies

```bash
pip install -r requirements.txt
```
## Usage

```python
import harvester

#Create a new harvester instace 
harvester_1 = harvester.new(solver_type="recaptchav3", url="https://recaptcha-demo.appspot.com/recaptcha-v3-request-scores.php", site_key="6LdyC2cUAAAAACGuDKpXeDorzUDWXmdqeg-xy696", action="examples/v3scores")

#Start a new solve
captcha_token = harvester_1.solve(timeout=100)

print(captcha_token)

```

## Working on

- Proxy support

- Support for importing chrome profiles
