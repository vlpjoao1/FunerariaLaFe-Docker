function generar_reporte(){
	var parameters={
		'action':'search_report',
		'start_date':'2021-02-06',
		'end_date':'2021-02-07'
	}
	$('#tabla_reporte').DataTable({
		responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: parameters,
            dataSrc: ""
        },
        columndefs:[

        ],
        order: false,
        paging: false,
        ordering: false,
        info: false,
        searching: false,
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
}
$(function(){
	$('input[name="date_range"]').daterangepicker().daterangepicker({
		locale:{
			format: 'YYYY-MM-DD'
		}
	});
	generar_reporte();
});