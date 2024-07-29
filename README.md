## Installation

1. Fork this repository to your github account
2. Clone the forked repository and proceed with steps mentioned below

### Install requirements

```
virtualenv env --python=python3.8
source env/bin/activate
pip install -r requirements.txt
```
### Start Server

```
python server.py
```
After that open index.html file on your browser.

### To test if the application is working fine , create rule by using this example : 

```
(((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5))
```
### Create Rule : 

<img width="571" alt="Screenshot 2024-07-30 at 12 25 35 AM" src="https://github.com/user-attachments/assets/b7f4b627-2f3b-44dc-835f-001acacc1bbe">

### RESULTING ABSTRACT SYNTAX TREE : 

<img width="433" alt="Screenshot 2024-07-30 at 12 26 57 AM" src="https://github.com/user-attachments/assets/6d9166cb-9385-4103-8c69-4327260250ec">

### Combining Rules : 

<img width="522" alt="Screenshot 2024-07-30 at 12 27 39 AM" src="https://github.com/user-attachments/assets/194b3fae-4f25-44ce-ae1f-c98255d149d7">

### RESULTING COMBINED SYNTAX TREE :

<img width="425" alt="Screenshot 2024-07-30 at 12 28 23 AM" src="https://github.com/user-attachments/assets/a70adc91-14a9-4d9b-b42d-32e6db933cdd">

## Visualizing JSON format into TREE format : 

<img width="1440" alt="Screenshot 2024-07-30 at 12 12 16 AM" src="https://github.com/user-attachments/assets/5c23cf40-3462-4a1e-ae60-000d9009b576">



