# Abstract All the Things

## Instructions

### Prepare the environment

```
git clone git@github.com:dravetech/preso_abstract_all_the_things.git
mkvirtualenv -a preso_abstract_all_the_things preso_abstract_all_the_things
pip install -r requirements.txt
```

### Start the lab

For this preso I used an online lab hosted by [network.toCode()](https://labs.networktocode.com/). The lab name is `MULTI-VENDOR EOS (2) AND VMX (2)`. If you want to try it out [network.toCode()](http://networktocode.com/) has been kindly enough to provide a promotion code: `napalm6`. The promotion code will let you run the lab at least once.

> Note: Neither me or my employer are in any way affiliated with [network.toCode()](http://networktocode.com/).

### Configuring the environment

After the lab is started and before actually starting to work with the demo you will have to configure your environment. To do so gather the following information:

 1. Lab IP's. You can find them under "Console and IP information" in your lab dashboard.
 1. Slack channel name. You will need a slack channel to do some bits of the demo. If you don't want to test this part you can skip this.
 1. You will have to enable `hubot` on your slack channel and get a token so you can use it. If you don't want to test this part you can skip this.

 When you have all the needed information execute the script `configure_environment.sh`:

```
 (preso_abstract_all_the_things) ➜  preso_abstract_all_the_things git:(master) ✗ ./configure_environment.sh
Enter the IP vmx1: 10.23.12.4
Enter the IP vmx2: 10.34.23.65
Enter the IP eos-spine1: 10.31.46.91
Enter the IP eos-spine1: 10.35.12.46
Enter your slack channel name: chatops_demo_dbarroso
Enter your slack token: xoxb-37241085586-wYkAvn1Tw58vQLDfake
```

### Start ST2

This part is only necessary if you want to test the slack integration and the API. To start the vagrant box execute:

```
VAGRANT_CWD=./tests/test_helpers/vagrant vagrant start
```

Note the IP that was given to the box once it's up and running.

#### Stop ST2

When you are done and you want to stop the box execute:

```
VAGRANT_CWD=./tests/test_helpers/vagrant vagrant destroy
```
