from django.db import models
from django.contrib.auth.models import User


class BaseModel(models.Model):
    class Meta:
        abstract = True

    user = models.ForeignKey(User)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


class Operacao(BaseModel):

    COMPRA_VENDA_CHOICE = (
        ('C', 'Compra'),
        ('V', 'Venda'),
    )

    #PRAZO_CHOICE = (
    #    ('DT', 'Day Trade'),
    #    ('ON', 'Operação Normal'),
    #)

    BOLSA_CHOICE = (
        ('AV', 'Ações - à Vista - BOVESPA'),
        ('OV', 'Opções - à Vista - BOVESPA'),
        ('MIF', 'Mini-Indice - Futuro - BM&F'),
    )

    encerrada = models.BooleanField(default=False)
    c_v = models.CharField(max_length=1, choices=COMPRA_VENDA_CHOICE)

    # TODO: Futuros e opcoes
    # prazo = models.CharField(max_length=2, choices=PRAZO_CHOICE)

    tipo_ativo = models.CharField(max_length=3, choices=BOLSA_CHOICE)
    ativo = models.CharField(max_length=10)
    timestamp_executou = models.DateTimeField()
    quantidade = models.PositiveIntegerField()
    preco = models.DecimalField(max_digits=6, decimal_places=2)
    corretagem = models.DecimalField(max_digits=6, decimal_places=2)
    emolumentos = models.DecimalField(max_digits=6, decimal_places=2)

    def save(self, *args, **kwargs):
        super(Operacao, self).save(*args, **kwargs)

    @property
    def acc_quantidade(self):
        return self.quantidade if self.c_v == 'C' else -self.quantidade

# TODO
def antes_de_salvar(new_op):

    ops_ativas = Operacao.objects.filter(ativo=new_op.ativo, encerrada=False).order_by('timestamp_executou')
    quantidade_acc = sum(op.acc_quantidade for op in ops_ativas)

    if quantidade_acc + new_op.acc_quantidade == 0:
        # Zerou
        # encerra todas operacoes
        pass

    # Mesmo sinal
    elif (quantidade_acc > 0) == (new_op.acc_quantidade > 0):
        # Aumentou a posicao
        pass

    # Sinal diferentes
    else:
        # cria uma operacao com 'quantidade_acc'
        # encerra todas operacoes

        # cuidado, caso realização parcial/virada de mão.
        diff = quantidade_acc + new_op.acc_quantidade
        if diff:
            new_op.quantidade = diff


class FechamentoMensal(BaseModel):
    mes = models.DateField()
    lucro_bruto = models.DecimalField(max_digits=6, decimal_places=2)
    custos = models.DecimalField(max_digits=6, decimal_places=2)
    imposto = models.DecimalField(max_digits=6, decimal_places=2)
    lucro_liquido = models.DecimalField(max_digits=6, decimal_places=2)
    acumulado = models.DecimalField(max_digits=6, decimal_places=2)
