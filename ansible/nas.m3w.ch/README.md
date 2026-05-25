```bash
ansible-playbook ansible/nas.m3w.ch/playbook.yaml \
    --inventory 192.168.1.2, \
    --user debian \
    --ask-pass \
    --ask-become-pass \
    --extra-vars "@ansible/nas.m3w.ch/variables.yaml"
```
