// $(document).ready(function () {
//   $('#water_quality_data_table').DataTable({
//       ajax: {
//           url: '/water_quality_data',
//           dataSrc: 'data'
//       },
//       columns: [
//           { data: 'Location ID' },
//           { data: 'Location Name' },
//           { data: 'Date' },
//           { data: 'Spec_Cond_Max' },
//           { data: 'PH_Max' },
//           { data: 'PH_Min' },
//           { data: 'Spec_Cond_Min' },
//           { data: 'Spec_Cond_Mean' },
//           { data: 'Dissolved_Oxy_Max' },
//           { data: 'Dissolved_Oxy_Mean' },
//           { data: 'Dissolved_Oxy_Min' },
//           { data: 'Temp Mean' },
//           { data: 'Temp Min' },
//           { data: 'Temp Max' },
//           { data: 'Training' },
//           { data: 'Water Quality' },
//       ],

//   })

//   /*$.getJSON('/water_quality_data', function (data) {
//       $('#water_quality_data_table').DataTable({
//           data: data,
//           columns: [
//               { data: 'Location ID' },
//               { data: 'Location Name' },
//               { data: 'Date' },
//               { data: 'Spec_Cond_Max' },
//               { data: 'PH_Max' },
//               { data: 'PH_Min' },
//               { data: 'Spec_Cond_Min' },
//               { data: 'Spec_Cond_Mean' },
//               { data: 'Dissolved_Oxy_Max' },
//               { data: 'Dissolved_Oxy_Mean' },
//               { data: 'Dissolved_Oxy_Min' },
//               { data: 'Temp Mean' },
//               { data: 'Temp Min' },
//               { data: 'Temp Max' },
//               { data: 'Training' },
//               { data: 'Water Quality' },
//           ],
//           // Define table columns (modify as needed based on your water_quality_data model)
//       })  // Add more columns as needed for other water quality data fields

//   });
//   */
// });