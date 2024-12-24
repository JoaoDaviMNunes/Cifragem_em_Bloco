eval "$(ssh-agent -s)"
#ssh-add ~/.ssh/id_ed25519
rm saida.txt
rm final.txt
python3 blocks_coder.py
python3 blocks_decoder.py
echo "Script realizado"