$ = require("jquery");

module.exports = function(inst){
  logo_graphic.bind('click', function (e) {
    var hmm_logo = logo,
    info_tab = $('<table class="logo_col_info"></table>'),
    header = '<tr>',
    tbody  = '',
    offset = inst.$el.offset(),
    x = parseInt((e.pageX - offset.left), 10),

    // get mouse position in the window
    window_position = e.pageX - inst.$el.parent().offset().left,

    // get column number
    col = hmm_logo.columnFromCoordinates(x),
    // clone the column data before reversal or the column gets messed
    // up in the logo when zoom levels change. Also stops flip-flopping
    // of the order from ascending to descending.
    col_data = [],
    info_cols = 0,
    i = 0,
    j = 0,
    height_header = 'Probability';

    if (logo.data.height_calc && logo.data.height_calc === 'score') {
      height_header = 'Score';
      col_data = logo.data.heightArr[col - 1].slice(0).reverse();
    } else {
      col_data = logo.data.probs_arr[col - 1].slice(0).reverse();
    }

    info_cols = Math.ceil(col_data.length / 5);
    //add the headers for each column.
    for (i = 0; i < info_cols; i++) {
      // using the i < info_cols - 1 check to make sure the last column doesn't
      // get marked with the odd class so we don't get a border on the edge of the table.
      if (info_cols > 1 && i < (info_cols - 1)) {
        header += '<th>Residue</th><th class="odd">' + height_header + '</th>';
      } else {
        header += '<th>Residue</th><th>' + height_header + '</th>';
      }
    }


    header += '</tr>';
    info_tab.append($(header));

    // add the data for each column
    for (i = 0; i < 5; i++) {
      tbody += '<tr>';
      j = i;
      while (col_data[j]) {
        var values = col_data[j].split(':', 2),
        color = '';
        if (logo.colorscheme === 'default') {
          color = logo.alphabet + '_' + values[0];
        }
        // using the j < 15 check to make sure the last column doesn't get marked
        // with the odd class so we don't get a border on the edge of the table.
        if (info_cols > 1  &&  j < 15) {
          tbody += '<td class="' + color + '"><div></div>' + values[0] + '</td><td class="odd">' + values[1] + '</td>';
        } else {
          tbody += '<td class="' + color + '"><div></div>' + values[0] + '</td><td>' + values[1] + '</td>';
        }

        j += 5;
      }
      tbody += '</tr>';
    }

    info_tab.append($(tbody));

    $(options.column_info).empty()
    .append($('<p> Column:' + col  + '</p><div><p>Occupancy: ' + logo.data.delete_probs[col - 1] + '</p><p>Insert Probability: ' + logo.data.insert_probs[col - 1] + '</p><p>Insert Length: ' + logo.data.insert_lengths[col - 1] + '</p></div>'))
    .append(info_tab).show();
  });
}
