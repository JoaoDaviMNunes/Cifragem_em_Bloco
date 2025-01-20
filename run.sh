#eval "$(ssh-agent -s)"
#ssh-add ~/.ssh/id_ed25519
rm saida.txt
rm final.txt
python3 completo.py entrada.txt saida.txt chave.txt cifragem
python3 completo.py saida.txt final.txt chave.txt decifragem
echo "Script finalizado"