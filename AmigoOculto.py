import random


class AmigoOculto:
    def __init__(self) -> None:
        """
        Inicializa a classe AmigoOculto com listas para participantes, telefones, uma lista auxiliar e o dicionário de sorteio.
        """
        self.participantes = []
        self.telefones = []
        self.auxiliar = []
        self.sorteio = {}

    def inserir_participante(self, participantes_dict):
        """
        Insere participantes e telefones da entrada do dicionário.

        Args:
            participantes_dict (dict): Dicionário contendo nomes de participantes e seus respectivos telefones.

        Returns:
            None
        """
        self.participantes_dict = participantes_dict
        for nome, telefone in participantes_dict.items():
            self.participantes.append(nome)
            self.telefones.append(telefone)

        self.auxiliar = self.participantes.copy()

    def embaralhar_participantes(self):
        """
        Embaralha a lista de participantes.

        Returns:
            None
        """
        random.shuffle(self.participantes)

    def sortear(self):
        """
        Realiza o sorteio dos participantes e seus amigos ocultos.

        Returns:
            None
        """
        # Flag para indicar se o sorteio foi bem-sucedido
        self.funcionou = True

        # Embaralha a lista de participantes
        self.embaralhar_participantes()

        # Loop para realizar o sorteio
        for participante in self.participantes:
            sorteado = random.choice(self.auxiliar)

            # Garante que o participante não tire ele mesmo e lida com casos de impossibilidade de sorteio
            while sorteado == participante:
                sorteado = random.choice(self.auxiliar)
                if len(self.auxiliar) == 1:
                    self.funcionou = False
                    break

            # Adiciona o sorteado ao dicionário de sorteio
            self.auxiliar.remove(sorteado)
            self.sorteio[participante] = {
                'amigoX': sorteado,
                'telefone': self.participantes_dict[participante],
            }

        # Se o sorteio não foi bem-sucedido, reinicia o processo
        if not self.funcionou:
            self.auxiliar = self.participantes.copy()
            self.sortear()
