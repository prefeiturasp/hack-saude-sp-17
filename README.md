# Big Data Saúde

## ChatBot

A interação com o usuário é feita pela Vivi, um ChatBot para Messenger desenvolvido através de [api.ai](https://api.ai/) e integrado com a page do Facebook.
Ela segue o Procedimento Operacional Padrão descrito na seção **5.2.4.6 Medicamentos** encontrada [neste link](ftp://ftp.saude.sp.gov.br/ftpsessp/bibliote/informe_eletronico/2016/iels.out.16/Iels196/M_PT-SMS-1875_2016.pdf).

## Back-end

O Back-end, desenvolvido em Python, cuidaria da lógica da Vivi a partir das respostas dadas a ela, mas não pôde ser implementado por limitações técnicas e problemas de documentação da api.ai.
Foi feito deploy como webhook no Heroku na URL seguinte: https://hack-saude-sp-17.herokuapp.com/webhook