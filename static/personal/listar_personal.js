var $= jQuery.noConflict();
function listadoPersonal(){
	$.ajax({
		url:"/Personal/Listar/",
		type:"get",
		dataType:"json",
		success: function(response){
			console.log(response);
			$('#columna_de_cartas').html("");
			for(let i=0; i < response.length; i++){
				let fila = '<div class="card">';
				fila += '<img class="card-img-top" src="/media/'+response[i]['fields']['foto']+'" alt="Card image cap">';
				fila += '<div class="card-body">';
				fila += '<h5 class="card-title">'+response[i]['fields']['apellidos']+', '+response[i]['fields']['nombres']+'</h5>';
				if (response[i]['fields']['telefono']==null){
					fila += '<p class="card-text">Teléfono:Desconocido</p>';
				}else{
				fila += '<p class="card-text">Teléfono:'+response[i]['fields']['telefono']+'</p>';
				}
				fila += '<p class="card-text">Ingreso:'+response[i]['fields']['fecha_de_ingreso']+'</p>';
				if(response[i]['fields']['direccion']==null){
					fila += '<p class="card-text">Dirección:Desconocida</p>';
				}else{
					fila += '<p class="card-text">Dirección:'+response[i]['fields']['direccion']+'</p>';
				}
				fila += '<div>';
				fila += '<div class="card-footer">';
				fila += '<center><button type="button" class="btn btn-danger btn-sm">Eliminar</button> <button type="button" onclick="abrir_modal_edicion(\'/Personal/Actualizar/'+response[i]['pk']+'/\')" class="btn btn-primary btn-sm">Modificar</button></center>'
				fila += '<div>';
				fila += '</div>';

				$('#columna_de_cartas').append(fila);
			}
		},
		error: function(error){
			console.log(error);
		}
	});
}

$(document).ready(function(){
	listadoPersonal();
});

function crear_personal(url){
	$('#crear_personal').load(url,function(){
		$(this).modal('show');
	});
}
function cerrar_modal(){
	$('#crear_personal').modal('hide');
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
	if(errores.responseJSON.error.ci_rif){
		error+='<div class="alert alert-danger"><strong>Cédula del cliente: '+errores.responseJSON.error.ci_rif+' </strong></div>';
	}	
	if(errores.responseJSON.error.nombre_cliente){
		error+='<div class="alert alert-danger"><strong>Nombre del cliente: '+errores.responseJSON.error.nombre_cliente+' </strong></div>';
	}
	if(errores.responseJSON.error.tipo_cliente){
		error+='<div class="alert alert-danger"><strong>Tipo de cliente: '+errores.responseJSON.error.tipo_cliente+' </strong></div>';
	}
	if(errores.responseJSON.error.telefono_cliente){
		error+='<div class="alert alert-danger"><strong>Teléfono del cliente: '+errores.responseJSON.error.telefono_cliente+' </strong></div>';
	}
	if(errores.responseJSON.error.domicilio_cliente){
		error+='<div class="alert alert-danger"><strong>Domicilio del cliente: '+errores.responseJSON.error.domicilio_cliente+' </strong></div>';
	}
	$('#errores_creacion').append(error)
}

function registrar_personal(){
	$.ajax({
		data:$('#creacion_form').serialize(),
		url:$('#creacion_form').attr('action'),
		type:$('#creacion_form').attr('method'),	
		success: function(response){
			BloquearBoton();
			notificationSuccess(response.mensaje);
			cerrar_modal();
			listadoPersonal();
		},
		error: function(error){
			console.log(error.responseJSON);
			notificationError(error.responseJSON.mensaje);
			mostrar_errores_creacion(error);
		}
	});
}
{}
function abrir_modal_edicion(url){
	$('#editar_personal').load(url,function(){
		$(this).modal('show');
	});
}

function cerrar_modal_edicion(){
	$('#editar_personal').modal('hide');
}

function bloquear_boton_edicion(){
	if($('#boton_edicion').prop('disabled')){
		$('#boton_edicion').prop('disabled',false);
	}else{
		$('#boton_edicion').prop('disabled',true);
	}
}

function editar_personal(){
	$.ajax({
		data:$('#edicion_form').serialize(),
		url:$('#edicion_form').attr('action'),
		type:$('#edicion_form').attr('method'),
		success: function(response){
			bloquear_boton_edicion();
			notificationSuccess(response.mensaje);
			listadoclientes();
			cerrar_modal_edicion();
		},
		error: function(error){
			notificationError(error.responseJSON.mensaje);
			mostrar_errores_creacion(error);
		}
	});
}
