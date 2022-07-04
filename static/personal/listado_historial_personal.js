var $= jQuery.noConflict();

function listadoHistorial(){
	$.ajax({
		url:"/Personal/Historial/Listar/",
		type:"get",
		dataType:"json",
		success: function(response){
			if ($.fn.DataTable.isDataTable('#tabla_historial')){
				$('#tabla_historial').DataTable().destroy();
			}
			console.log(response);
			$('#tabla_historial tbody').html("");
			for(let i=0; i < response.length; i++){
				let fila = '<tr>';
				fila += '<td>' + (i+1) + '</td>';
				fila += '<td>' + response[i]['fields']['historial_empleado'] + '</td>';
				fila += '<td>' + response[i]['fields']['acotacion'] + '</td>';
				fila += '<td>' + response[i]['fields']['fecha_acotacion'] + '</td>';
				fila += '<td><center><button type="button" class="btn btn-success btn-sm" ';
				fila += 'onclick="abrir_modal_edicion(\'/Personal/Historial/Editar/'+response[i]['pk']+'/\'); ">EDITAR</button>';	

				fila += ' <button type="button" class="btn btn-danger btn-sm" ';
				fila += 'onclick="modal_eliminar(\'/Personal/Historial/Eliminar/'+response[i]['pk']+'/\'); ">ELIMINAR</button>';

				fila += '</center></td>';
				fila += '</tr>';

				$('#tabla_historial tbody').append(fila);
			}
			$('#tabla_historial').DataTable({
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
	listadoHistorial();
});

function crear_historial_personal(url){
	$('#crear_historial').load(url,function(){
		$(this).modal('show');
	});
}
function cerrar_modal(){
	$('#crear_historial').modal('hide');
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
	if(errores.responseJSON.error.historial_empleado){
		error+='<div class="alert alert-danger"><strong>Empleado: '+errores.responseJSON.error.historial_empleado+' </strong></div>';
	}	
	if(errores.responseJSON.error.acotacion){
		error+='<div class="alert alert-danger"><strong>Acotación: '+errores.responseJSON.error.acotacion+' </strong></div>';
	}
	if(errores.responseJSON.error.fecha_acotacion){
		error+='<div class="alert alert-danger"><strong>Fecha:'+errores.responseJSON.error.fecha_acotacion+' </strong></div>';
	}

	$('#errores_creacion').append(error)
}

function registrar_historial(){
	$.ajax({
		data:$('#creacion_form').serialize(),
		url:$('#creacion_form').attr('action'),
		type:$('#creacion_form').attr('method'),
		success: function(response){
			BloquearBoton();
			notificationSuccess(response.mensaje);
			cerrar_modal();
			listadoHistorial();
		},
		error: function(error){
			notificationError(error.responseJSON.mensaje);
			mostrar_errores_creacion(error);
		}
	});
}

function abrir_modal_edicion(url){
	$('#editar_historial').load(url,function(){
		$(this).modal('show');
	});
}
function cerrar_modal_edicion(){
	$('#editar_historial').modal('hide');
}
function bloquear_boton_edicion(){
	if($('#boton_edicion').prop('disabled')){
		$('#boton_edicion').prop('disabled',false);
	}else{
		$('#boton_edicion').prop('disabled',true);
	}
}

function editar_historial(){
	$.ajax({
		data:$('#edicion_form').serialize(),
		url:$('#edicion_form').attr('action'),
		type:$('#edicion_form').attr('method'),
		success: function(response){
			bloquear_boton_edicion();
			notificationSuccess(response.mensaje);
			listadoHistorial();
			cerrar_modal_edicion();
		},
		error: function(error){
			notificationError(error.responseJSON.mensaje);
			mostrar_errores_creacion(error);
		}
	});
}
function modal_eliminar(url){
	$('#eliminar_historial').load(url,function(){
		$(this).modal('show');
	});
} 
function cerrar_modal_eliminar(){
	$('#eliminar_historial').modal('hide');
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
		url: '/Personal/Historial/Eliminar/'+pk+'/',
		type: 'post',
		success: function(response){
			BloquearBotonEliminar();	
			notificationSuccess(response.mensaje);
			listadoHistorial();
			cerrar_modal_eliminar();
		},
		error: function(error){
			notificationError(error.responseJSON.mensaje);
		}
	});
} 	