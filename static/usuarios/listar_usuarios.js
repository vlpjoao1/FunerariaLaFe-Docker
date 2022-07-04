var $= jQuery.noConflict();

function listadoUsuarios(){
	$.ajax({
		url:"/Users/Listar/",
		type:"get",
		dataType:"json",
		success: function(response){
			if ($.fn.DataTable.isDataTable('#tabla_usuario')){
				$('#tabla_usuario').DataTable().destroy();
			}
			$('#tabla_usuario tbody').html("");
			console.log(response);
			for(let i=0; i < response.length; i++){
				let fila = '<tr>';
				fila += '<td>' + (i+1) + '</td>';
				fila += '<td>'+response[i]['fields']['nombre']+', '+response[i]['fields']['apellidos']+'</td>';
				fila += '<td>' + response[i]['fields']['email'] + '</td>';
				fila += '<td>' + response[i]['fields']['username'] + '</td>';
				if(response[i]['fields']['is_superuser']==true){
					fila += '<td>Super usuario</td>';
				}else{	
					fila += '<td>Usuario normal</td>';
				}
				fila += '<td><center><button type="button" class="btn btn-success btn-sm" ';
				fila += 'onclick="abrir_modal_edicion(\'/Users/Editar/'+response[i]['pk']+'/\'); ">EDITAR</button>';	

				fila += ' <button type="button" class="btn btn-danger btn-sm" ';
				fila += 'onclick="modal_eliminar(\'/Users/Eliminar/'+response[i]['pk']+'/\'); ">ELIMINAR</button>';

				fila += '</center></td>';
				fila += '</tr>';

				$('#tabla_usuario tbody').append(fila);
			}
			$('#tabla_usuario').DataTable({
				language: {
					decimal: "",
					emptyTable: "No hay información",
					info: "Mostrando _START_ a _END_ de _TOTAL_ Entradas",
					infoEmpty: "Mostrando 0 to 0 of 0 Entradas",
					infoFiltered: "(Filtrado de _MAX_ total entradas)",
					infoPostFix: "",
					thousands: ",",
					lengthMenu: "Mostrar _MENU_ Entradas",
					loadingRecords: "Cargando...",
					processing: "Procesando...",
					search: "Buscar:",
					zeroRecords: "Sin resultados encontrados",
					paginate: {
						first: "Primero",
						last: "Ultimo",
						next: "Siguiente",
						previous: "Anterior",
					},
				},	
			});
		},
		error: function(error){
			console.log(error);
		}
	});
}
$(document).ready(function(){
	listadoUsuarios();
});


function crear_usuario(url){
	$('#crear_usuario').load(url,function(){
		$(this).modal('show');
	});
}
function cerrar_modal(){
	$('#crear_usuario').modal('hide');
}
function BloquearBoton(){
	if($('#boton_creacion').prop('disabled')){
		$('#boton_creacion').prop('disabled',false);
	}else{
		$('#boton_creacion').prop('disabled',true);
	}
}
function notificationError(mensaje){
	Swal.fire({
		title:'Error',
		text:mensaje,
		icon:'error'
	})
}
function notificationSuccess(mensaje){
	Swal.fire({
		title:'Buen trabajo',
		text:mensaje,
		icon:'success'
	})
}

function mostrar_errores_creacion(errores){
	$('#errores_creacion').html("");
	let error="";
	if(errores.responseJSON.error.username){
		error+='<div class="alert alert-danger"><strong>username: '+errores.responseJSON.error.username+' </strong></div>';
	}	
	if(errores.responseJSON.error.pregunta){
		error+='<div class="alert alert-danger"><strong>Pregunta de seguridad: '+errores.responseJSON.error.pregunta+' </strong></div>';
	}
	if(errores.responseJSON.error.respuesta){
		error+='<div class="alert alert-danger"><strong>Respuesta de seguridad: '+errores.responseJSON.error.respuesta+' </strong></div>';
	}
	if(errores.responseJSON.error.is_superuser){
		error+='<div class="alert alert-danger"><strong>¿Es superusuario?: '+errores.responseJSON.error.is_superuser+' </strong></div>';
	}
	if(errores.responseJSON.error.password2){
		error+='<div class="alert alert-danger"><strong>Contraseña: '+errores.responseJSON.error.password2+' </strong></div>';
	}
	$('#errores_creacion').append(error)
}
function valida_password(){
	var pass = document.getElementsByName("password1");
	var pas1 = pass[0].value;
	if (pas1.length > 7 || pas1.length < 17)
	{
		var mayuscula=false;
		var minuscula=false;
		var numero=false;
		var caracter_raro=false;

		for (var i = 0; i<pas1.length; i++)
		{
			if(pas1.charCodeAt(i)>=65 && pas1.charCodeAt(i)<=90)
			{
				mayuscula=true;
			}
			else if(pas1.charCodeAt(i)>=97 && pas1.charCodeAt(i)<=122)
			{
				minuscula=true;
			}
			else if(pas1.charCodeAt(i)>=48 && pas1.charCodeAt(i)<=57)
			{
				numero=true;
			}else{
				caracter_raro=true;
			}
		}

		if(mayuscula==true && minuscula==true && caracter_raro==true && numero==true)
		{
			return true;	
		}else{
			var mensaje='La contraseña debe contener al menos una letra mayuscula, minuscula y 1 número.';
		return [false,mensaje];
		}

	}else{
		var mensaje='La contraseña debe ser mayor a 8 y menor de 16 digitos';
		return [false,mensaje];
	}
}
function registrar_usuario(){
	$.ajax({
		data:$('#creacion_form').serialize(),
		url:$('#creacion_form').attr('action'),
		type:$('#creacion_form').attr('method'),
		success: function(response){
			BloquearBoton();
			notificationSuccess(response.mensaje);
			cerrar_modal();
			listadoUsuarios();
		},
		error: function(error){
			notificationError(error.responseJSON.mensaje);
			mostrar_errores_creacion(error);
		}
	});
}
function pre_registrar(){
	var validacion = valida_password();
	//al notificationSucces, le pasarás el mensaje que 
	//usará como parámetro que se mostrará en el popup
	if (validacion==true){
		registrar_usuario();
	}else if(validacion[0]==false){
		notificationError(validacion[1]);
	}
}

function pre_editar(){
	var validacion = valida_password();
	//al notificationSucces, le pasarás el mensaje que 
	//usará como parámetro que se mostrará en el popup
	if (validacion==true){
		editar_usuario();
	}else if(validacion[0]==false){
		notificationError(validacion[1]);
	}
}

function abrir_modal_edicion(url){
	$('#editar_usuario').load(url,function(){
		$(this).modal('show');
	});
}
function cerrar_modal_edicion(){
	$('#editar_usuario').modal('hide');
}
function bloquear_boton_edicion(){
	if($('#boton_edicion').prop('disabled')){
		$('#boton_edicion').prop('disabled',false);
	}else{
		$('#boton_edicion').prop('disabled',true);
	}
}

function editar_usuario(){
	$.ajax({
		data:$('#edicion_form').serialize(),
		url:$('#edicion_form').attr('action'),
		type:$('#edicion_form').attr('method'),
		success: function(response){
			bloquear_boton_edicion();
			notificationSuccess(response.mensaje);
			listadoUsuarios();
			cerrar_modal_edicion();
		},
		error: function(error){
			notificationError(error.responseJSON.mensaje);
			mostrar_errores_creacion(error);
		}
	});
}
function modal_eliminar(url){
	$('#eliminar_usuario').load(url,function(){
		$(this).modal('show');
	});
} 
function cerrar_modal_eliminar(){
	$('#eliminar_usuario').modal('hide');
}
function BloquearBotonEliminar(){
	if($('#boton_eliminar').prop('disabled')){
		$('#boton_eliminar').prop('disabled',false);
	}else{
		$('#boton_eliminar').prop('disabled',true);
	}
}

function eliminar(pk){
	$.ajax({
		data:{
			csrfmiddlewaretoken:$("[name='csrfmiddlewaretoken']").val()
		},
		url: '/Users/Eliminar/'+pk+'/',
		type: 'post',
		success: function(response){
			BloquearBotonEliminar();	
			cerrar_modal_eliminar();
			notificationSuccess(response.mensaje);
			listadoUsuarios();
		},
		error: function(error){
			notificationError(error.responseJSON.mensaje);
		}
	});
} 	