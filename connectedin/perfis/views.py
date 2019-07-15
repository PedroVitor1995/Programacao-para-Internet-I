from perfis.models import *
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

# Create your views here.
@login_required
def index(request):
	return render(request, 'index.html',{'perfis': Perfil.objects.all(),
                   'perfil_logado' : get_perfil_logado(request)})

@login_required
def exibir_perfil(request, perfil_id):
	perfil = Perfil.objects.get(id=perfil_id)
	perfil_logado = get_perfil_logado(request)
	ja_eh_contato = perfil in perfil_logado.contatos.all()
	return render(request, 'perfil.html',{'perfil' : perfil,
                   'perfil_logado' : get_perfil_logado(request),
                   'ja_eh_contato':ja_eh_contato})

@login_required
def convidar(request, perfil_id):
	perfil_a_convidar = Perfil.objects.get(id=perfil_id)
	perfil_logado = get_perfil_logado(request)
	if perfil_logado.pode_convidar(perfil_a_convidar):
		perfil_logado.convidar(perfil_a_convidar)
		messages.success(request,'Convite foi enviado.')
	else:
		messages.error(request,'Não foi possivel enviar o convite.')

	return redirect('index')


@login_required
def get_perfil_logado(request):
	return request.user.perfil

@login_required
def aceitar(request, convite_id):
	convite = Convite.objects.get(id=convite_id)
	convite.aceitar()
	return redirect('index')

#Rejeitar solicitação
@login_required
def recusar(request, convite_id):
	convite = Convite.objects.get(id=convite_id)
	convite.recusar()
	return redirect('index')

#Desfazer amizade
@login_required
def desfazer(request,perfil_id):
	perfil_a_desfazer = Perfil.objects.get(id=perfil_id)
	perfil_logado = get_perfil_logado(request)
	perfil_logado.desfazer(perfil_a_desfazer)
	return redirect('index')
	 	
#Alterar senha
@login_required
def alterar_senha(request):
	if request.method == 'POST':
		form = PasswordChangeForm(request.user, request.POST)
		if form.is_valid():
			user = form.save()
			update_session_auth_hash(request, user)
			messages.success(request, 'Sua senha foi atualizada com sucesso.')
			return redirect('alterar_senha')
		else:
			senha_exists = User.objects.filter(password=request.POST['old_password']).exists()
			if senha_exists:
				messages.error(request,'A senha atual não confere.')

			elif request.POST['new_password2'] != request.POST['new_password1']:
				messages.error(request, 'A confirmação da senha não confere com a nova senha.')
			else:
				messages.error(request, 'Verifique seus dados.')

			

	else:
		form = PasswordChangeForm(request.user)

	return render(request, 'alterar_senha.html', {'perfil_logado' : get_perfil_logado(request),'form': form})

#Pesquisar usuário
@login_required
def pesquisar_usuario(request):
	perfis = Perfil.objects.all()
	perfil_logado = get_perfil_logado(request)
	nome_buscado = request.GET('nome')
	resultado = Perfil.objects.filter(nome__contains=nome_buscado) \
							.exclude(nome=perfil_logado.nome) \
							.exclude(bloqueado=True) \
							.exclude(ativo=False)
	contexto = {
		"perfil": perfil_logado,
		"resultado": resultado,
		"nome_buscado": nome_buscado
		}
	return render(request, 'busca.html', contexto)

