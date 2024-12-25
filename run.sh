#eval "$(ssh-agent -s)"
#ssh-add ~/.ssh/id_ed25519
rm saida.txt
rm final.txt
python3 blocks_coder.py entrada.txt saida.txt chave.txt
python3 blocks_decoder.py saida.txt final.txt chave.txt
echo "Script finalizado"