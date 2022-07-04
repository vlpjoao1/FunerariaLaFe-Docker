var $= jQuery.noConflict();

function listadoBitacora(){
	$.ajax({
		url:"/Personal/Bitacora/Listar/",
		type:"get",
		dataType:"json",
		success: function(response){
			if ($.fn.DataTable.isDataTable('#tabla_bitacora')){
				$('#tabla_bitacora').DataTable().destroy();
			}
			$('#tabla_bitacora tbody').html("");
			for(let i=0; i < response.length; i++){
				let fila = '<tr>';
				if(response[i]['fields']['si_trabajo']=="Si asistió"){
					fila += '<td class="text-dark">' + (i+1) + '</td>';
					fila += '<td class="text-dark">' + response[i]['fields']['empleado'] + '</td>';
					fila += '<td class="text-dark">' + response[i]['fields']['hora_entrada'] + ', '+response[i]['fields']['fecha_entrada']+'</td>';
					fila += '<td class="text-dark">' + response[i]['fields']['hora_salida'] + ', '+response[i]['fields']['fecha_salida']+'</td>';
					fila += '<td class="text-dark"><center><button type="button" class="btn btn-success btn-sm" ';
					fila += 'onclick="abrir_modal_edicion(\'/Personal/Bitacora/Editar/'+response[i]['pk']+'/\'); ">EDITAR</button>';	

					fila += ' <button type="button" class="btn btn-danger btn-sm" ';
					fila += 'onclick="modal_eliminar(\'/Personal/Bitacora/Eliminar/'+response[i]['pk']+'/\'); ">ELIMINAR</button>';

					fila += '</center></td>';
					fila += '</tr>';
				}else if(response[i]['fields']['si_trabajo']=="No asistió"){
					fila += '<td class="text-dark bg-warning">' + (i+1) + '</td>';
					fila += '<td class="text-dark bg-warning">' + response[i]['fields']['empleado'] + '</td>';
					fila += '<td class="text-dark bg-warning">No asistió la fecha '+response[i]['fields']['fecha_entrada']+'</td>';
					fila += '<td class="text-dark bg-warning">No asistió la fecha '+response[i]['fields']['fecha_entrada']+'</td>';
					fila += '<td class="text-dark bg-warning"><center><button type="button" class="btn btn-success btn-sm" ';
					fila += 'onclick="abrir_modal_edicion(\'/Personal/Bitacora/Editar/'+response[i]['pk']+'/\'); ">EDITAR</button>';	

					fila += ' <button type="button" class="btn btn-danger btn-sm" ';
					fila += 'onclick="modal_eliminar(\'/Personal/Bitacora/Eliminar/'+response[i]['pk']+'/\'); ">ELIMINAR</button>';

					fila += '</center></td>';
					fila += '</tr>';

				};

				$('#tabla_bitacora tbody').append(fila);
			}
			$('#tabla_bitacora').DataTable({
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
	listadoBitacora();
});

function crear_bitacora_personal(url){
	$('#crear_bitacora').load(url,function(){
		$(this).modal('show');
	});
}
function cerrar_modal(){
	$('#crear_bitacora').modal('hide');
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
	if(errores.responseJSON.error.empleado){
		error+='<div class="alert alert-danger"><strong>Empleado: '+errores.responseJSON.error.empleado+' </strong></div>';
	}	
	if(errores.responseJSON.error.si_trabajo){
		error+='<div class="alert alert-danger"><strong>¿Asistió?: '+errores.responseJSON.error.si_trabajo+' </strong></div>';
	}
	if(errores.responseJSON.error.hora_entrada){
		error+='<div class="alert alert-danger"><strong>Fecha/Hora de entrada: '+errores.responseJSON.error.hora_entrada+' </strong></div>';
	}
	if(errores.responseJSON.error.hora_salida){
		error+='<div class="alert alert-danger"><strong>Fecha/Hora de salida: '+errores.responseJSON.error.hora_salida+' </strong></div>';
	}
	$('#errores_creacion').append(error)
}

function registrar_bitacora(){
	$.ajax({
		data:$('#creacion_form').serialize(),
		url:$('#creacion_form').attr('action'),
		type:$('#creacion_form').attr('method'),
		success: function(response){
			BloquearBoton();
			notificationSuccess(response.mensaje);
			cerrar_modal();
			listadoBitacora();
		},
		error: function(error){
			notificationError(error.responseJSON.mensaje);
			mostrar_errores_creacion(error);
		}
	});
}

function abrir_modal_edicion(url){
	$('#editar_bitacora').load(url,function(){
		$(this).modal('show');
	});
}
function cerrar_modal_edicion(){
	$('#editar_bitacora').modal('hide');
}
function bloquear_boton_edicion(){
	if($('#boton_edicion').prop('disabled')){
		$('#boton_edicion').prop('disabled',false);
	}else{
		$('#boton_edicion').prop('disabled',true);
	}
}

function editar_bitacora(){
	$.ajax({
		data:$('#edicion_form').serialize(),
		url:$('#edicion_form').attr('action'),
		type:$('#edicion_form').attr('method'),
		success: function(response){
			bloquear_boton_edicion();
			notificationSuccess(response.mensaje);
			listadoBitacora();
			cerrar_modal_edicion();
		},
		error: function(error){
			notificationError(error.responseJSON.mensaje);
			mostrar_errores_creacion(error);
		}
	});
}

function modal_eliminar(url){
	$('#eliminar_bitacora').load(url,function(){
		$(this).modal('show');
	});
} 
function cerrar_modal_eliminar(){
	$('#eliminar_bitacora').modal('hide');
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
		url: '/Personal/Bitacora/Eliminar/'+pk+'/',
		type: 'post',
		success: function(response){
			BloquearBotonEliminar();	
			cerrar_modal_eliminar();
			notificationSuccess(response.mensaje);
			listadoBitacora();
		},
		error: function(error){
			notificationError(error.responseJSON.mensaje);
		}
	});
} 	


function valida_formulario(){
	var entrada = document.getElementsByName("hora_entrada")[0].value;
	var fecha_entrada_dia = document.getElementById("id_fecha_entrada_day").value;
	var fecha_entrada_mes = document.getElementById("id_fecha_entrada_month").value;
	var fecha_entrada_año = document.getElementById("id_fecha_entrada_year").value;	

	var salida = document.getElementsByName("hora_salida")[0].value;
	var fecha_salida_dia = document.getElementById("id_fecha_salida_day").value;
	var fecha_salida_mes = document.getElementById("id_fecha_salida_month").value;
	var fecha_salida_año = document.getElementById("id_fecha_salida_year").value;

	var trabajo= document.getElementsByName("si_trabajo")[0].value;

	var valores = '1234567890';
	var punto = ':';

	var hora1='012';
	var hora2='0123456789';
	var hora2_2='0123';

	var minutos1='012345';
	var minutos2='0123456789';

	//entrada

	if(entrada[0]=='0' || entrada[0]=='1'){
		if(hora2.includes(entrada[1]) && entrada[2]==':' && minutos1.includes(entrada[3]) && minutos2.includes(entrada[4])){
			hora_entrada_validada=true;
		}else{
			hora_entrada_validada=false;
		}
	}else if(entrada[0]=='2'){
		if(hora2_2.includes(entrada[1]) && entrada[2]==':' && minutos1.includes(entrada[3]) && minutos2.includes(entrada[4])){
			hora_entrada_validada=true;
		}else{
			hora_entrada_validada=false;
		}
	}else{
		hora_entrada_validada=false;
	}

	if(fecha_entrada_dia!='' && fecha_entrada_mes!='' && fecha_entrada_año!=''){
		fecha_entrada_validada=true;
	}else{
		fecha_entrada_validada=false;
	}

	// salida
	if(salida[0]=='0' || salida[0]=='1'){
		if(hora2.includes(salida[1]) && salida[2]==':' && minutos1.includes(salida[3]) && minutos2.includes(salida[4])){
			hora_salida_validada=true;
		}else{
			hora_salida_validada=false;
		}
	}else if(salida[0]=='2'){
		if(hora2_2.includes(salida[1]) && salida[2]==':' && minutos1.includes(salida[3]) && minutos2.includes(salida[4])){
			hora_salida_validada=true;
		}else{
			hora_salida_validada=false;
		}
	}else{
		hora_salida_validada=false;
	}

	if(fecha_salida_dia!='' && fecha_salida_mes!='' && fecha_salida_año!=''){
		fecha_salida_validada=true;
	}else{
		fecha_salida_validada=false;
	}
	//validar fechasalida

	var entrada_dia=parseInt(fecha_entrada_dia);
	var entrada_mes=parseInt(fecha_entrada_mes);
	var entrada_año=parseInt(fecha_entrada_año);

	var salida_dia=parseInt(fecha_salida_dia);
	var salida_mes=parseInt(fecha_salida_mes);
	var salida_año=parseInt(fecha_salida_año);

	var dateentrada= new Date([entrada_año,entrada_mes,entrada_dia]);
	var datesalida= new Date([salida_año,salida_mes,salida_dia]);



	if(trabajo=='Si asistió'){
		if(hora_entrada_validada==true && fecha_entrada_validada==true && salida=='' && fecha_salida_dia=='' && fecha_salida_mes=='' && fecha_salida_año==''){
			registrar_bitacora();
		}else if(hora_entrada_validada==true && fecha_entrada_validada==true && hora_salida_validada==true && fecha_salida_validada==true){
			if(dateentrada.getTime()===datesalida.getTime() || dateentrada.getTime()<datesalida.getTime()){
				registrar_bitacora();
			}
			if(dateentrada.getTime()>datesalida.getTime()){
				$('#errores_creacion_fecha').html("");
				let error="";
				error+='<div class="alert alert-danger"><strong>La fecha de entrada es mayor que la de salida</strong></div>';
				$('#errores_creacion_fecha').append(error)
			}
		}else{
			$('#errores_creacion').html("");
			let error="";
			error+='<div class="alert alert-danger"><strong>Verifica que los campos estén rellenados correctamente.';
			error+=' Si solamente vas a registrar una entrada, debes rellenar los campos hora y fecha de entrada. Si deseas añadir una salida, los campos hora/fecha de entrada y salida debe estar llenos.</strong></div>';
			$('#errores_creacion').append(error)
		}
	}else if(trabajo=='No asistió'){
		if(entrada=='' && fecha_entrada_validada==true && salida=='' && fecha_salida_dia=='' && fecha_salida_mes=='' && fecha_salida_año==''){
			registrar_bitacora();
		}else{
			$('#errores_creacion').html("");
			let error="";
			error+='<div class="alert alert-danger"><strong>Debido a que seleccionaste "No asistió", solo deberás llenar los campos "Empleado" y "Fecha de entrada". Debes dejar los campos hora de entrada y hora/fecha de salida vacíos..</strong></div>';
			$('#errores_creacion').append(error)	
		}
	}
}
function valida_formulario_editar(){
	var entrada = document.getElementsByName("hora_entrada")[0].value;
	var fecha_entrada_dia = document.getElementById("id_fecha_entrada_day").value;
	var fecha_entrada_mes = document.getElementById("id_fecha_entrada_month").value;
	var fecha_entrada_año = document.getElementById("id_fecha_entrada_year").value;	

	var salida = document.getElementsByName("hora_salida")[0].value;
	var fecha_salida_dia = document.getElementById("id_fecha_salida_day").value;
	var fecha_salida_mes = document.getElementById("id_fecha_salida_month").value;
	var fecha_salida_año = document.getElementById("id_fecha_salida_year").value;

	var trabajo= document.getElementsByName("si_trabajo")[0].value;

	var valores = '1234567890';
	var punto = ':';

	var hora1='012';
	var hora2='0123456789';
	var hora2_2='0123';

	var minutos1='012345';
	var minutos2='0123456789';

	//entrada

	if(entrada[0]=='0' || entrada[0]=='1'){
		if(hora2.includes(entrada[1]) && entrada[2]==':' && minutos1.includes(entrada[3]) && minutos2.includes(entrada[4])){
			hora_entrada_validada=true;
		}else{
			hora_entrada_validada=false;
		}
	}else if(entrada[0]=='2'){
		if(hora2_2.includes(entrada[1]) && entrada[2]==':' && minutos1.includes(entrada[3]) && minutos2.includes(entrada[4])){
			hora_entrada_validada=true;
		}else{
			hora_entrada_validada=false;
		}
	}else{
		hora_entrada_validada=false;
	}

	if(fecha_entrada_dia!='' && fecha_entrada_mes!='' && fecha_entrada_año!=''){
		fecha_entrada_validada=true;
	}else{
		fecha_entrada_validada=false;
	}

	// salida
	if(salida[0]=='0' || salida[0]=='1'){
		if(hora2.includes(salida[1]) && salida[2]==':' && minutos1.includes(salida[3]) && minutos2.includes(salida[4])){
			hora_salida_validada=true;
		}else{
			hora_salida_validada=false;
		}
	}else if(salida[0]=='2'){
		if(hora2_2.includes(salida[1]) && salida[2]==':' && minutos1.includes(salida[3]) && minutos2.includes(salida[4])){
			hora_salida_validada=true;
		}else{
			hora_salida_validada=false;
		}
	}else{
		hora_salida_validada=false;
	}

	if(fecha_salida_dia!='' && fecha_salida_mes!='' && fecha_salida_año!=''){
		fecha_salida_validada=true;
	}else{
		fecha_salida_validada=false;
	}
	//validar fechasalida

	var entrada_dia=parseInt(fecha_entrada_dia);
	var entrada_mes=parseInt(fecha_entrada_mes);
	var entrada_año=parseInt(fecha_entrada_año);

	var salida_dia=parseInt(fecha_salida_dia);
	var salida_mes=parseInt(fecha_salida_mes);
	var salida_año=parseInt(fecha_salida_año);

	var dateentrada= new Date([entrada_año,entrada_mes,entrada_dia]);
	var datesalida= new Date([salida_año,salida_mes,salida_dia]);



	if(trabajo=='Si asistió'){
		if(hora_entrada_validada==true && fecha_entrada_validada==true && salida=='' && fecha_salida_dia=='' && fecha_salida_mes=='' && fecha_salida_año==''){
			editar_bitacora();
		}else if(hora_entrada_validada==true && fecha_entrada_validada==true && hora_salida_validada==true && fecha_salida_validada==true){
			if(dateentrada.getTime()===datesalida.getTime() || dateentrada.getTime()<datesalida.getTime()){
				editar_bitacora();
			}
			if(dateentrada.getTime()>datesalida.getTime()){
				$('#errores_creacion_fecha').html("");
				let error="";
				error+='<div class="alert alert-danger"><strong>La fecha de entrada es mayor que la de salida</strong></div>';
				$('#errores_creacion_fecha').append(error)
			}
		}else{
			$('#errores_creacion').html("");
			let error="";
			error+='<div class="alert alert-danger"><strong>Verifica que los campos estén rellenados correctamente.';
			error+=' Si solamente vas a registrar una entrada, debes rellenar los campos hora y fecha de entrada. Si deseas añadir una salida, los campos hora/fecha de entrada y salida debe estar llenos.</strong></div>';
			$('#errores_creacion').append(error)
		}
	}else if(trabajo=='No asistió'){
		if(entrada=='' && fecha_entrada_validada==true && salida=='' && fecha_salida_dia=='' && fecha_salida_mes=='' && fecha_salida_año==''){
			editar_bitacora();
		}else{
			$('#errores_creacion').html("");
			let error="";
			error+='<div class="alert alert-danger"><strong>Debido a que seleccionaste "No asistió", solo deberás llenar los campos "Empleado" y "Fecha de entrada". Debes dejar los campos hora de entrada y hora/fecha de salida vacíos..</strong></div>';
			$('#errores_creacion').append(error)	
		}
	}
}