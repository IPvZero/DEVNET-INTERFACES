# DEVNET-INTERFACES


This short lab pulls interface information from the Always-On IOSXE and IOSXR Sandboxes over NETCONF and prints the output in tabular form.


# Instructions
## 1) Clone this repository
```
git clone https://github.com/IPvZero/DEVNET-INTERFACES
```

## 2) Change into the DEVNET-INTERFACES directory
```
cd DEVNET-INTERFACES
```

## 3) Pip (or pip3) install the requirements

```
python3 -m pip install -r requirements.txt
```
  or 

```
pip3 install -r requirements.txt
```


## 4) Execute the script

```
python3 run1.py
```

## Output
![alt text](https://github.com/IPvZero/DEVNET-INTERFACES/blob/main/images/richpic.png?raw=true)


## You can SSH into each device manually using the following credentials
# IOSXE
```
ssh developer@sandbox-iosxe-latest-1.cisco.com
Password: C1sco12345
```

# IOSXR 
```
ssh admin@sbx-iosxr-mgmt.cisco.com -p 8181
Password: C1sco12345
```

### WARNING
You may log into each device and manually alter the configuration to change the outputs ie shutting and no shutting the interfaces/adding IP addresses.
However, in order to not erroneously alter critical settings be sure to issue a ```show run``` and read any interface descriptions.
My recommendation is to log into each device, add loopback interfaces and addresses and manually ```shut/no shut``` them. 
This will act as safeguard to avoid altering any MGMT connectivity configurations.

