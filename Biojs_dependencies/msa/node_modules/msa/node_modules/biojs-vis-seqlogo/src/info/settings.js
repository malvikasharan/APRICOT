var $ = require("jbone");

module.exports = function(logo,options){
  var form = $('<form class="logo_form"><fieldset><label for="position">Column number</label>' +
               '<input type="text" name="position" class="logo_position"></input>' +
               '<button class="button logo_change">Go</button></fieldset>' +
               '</form>');

  var settings = $('<div class="logo_settings"></div>');
  settings.append('<span class="close">x</span>');



  /* we don't want to toggle if the max height_obs is greater than max theoretical
   * as letters will fall off the top.
   */
  if (logo.scale_height_enabled && (logo.data.max_height_obs < logo.data.max_height_theory)) {
    var obs_checked = '',
    theory_checked = '',
    theory_help = '',
    obs_help = '';

    if (logo.data.max_height_obs === logo.data.max_height) {
      obs_checked = 'checked';
    } else {
      theory_checked = 'checked';
    }
  }



  var scale_controls = '<fieldset><legend>Scale</legend>' +
    '<label><input type="radio" name="scale" class="logo_scale" value="obs" ' + obs_checked +
    '/>Maximum Observed ' + obs_help +
    '</label></br>' +
    '<label><input type="radio" name="scale" class="logo_scale" value="theory" ' + theory_checked +
    '/>Maximum Theoretical ' + theory_help +
    '</label>' +
    '</fieldset>';

  settings.append(scale_controls);

  if (logo.data.height_calc !== 'score' && logo.data.alphabet === 'aa' && logo.data.probs_arr) {

    var def_color = null,
    con_color = null,
    def_help = '',
    con_help = '';

    if (logo.colorscheme === 'default') {
      def_color = 'checked';
    } else {
      con_color = 'checked';
    };

    if (options.help) {
      def_help = '<a class="help" href="/help#colors_default" title="Each letter receives its own color.">' +
        '<span aria-hidden="true" data-icon="?"></span><span class="reader-text">help</span></a>';
      con_help = '<a class="help" href="/help#colors_consensus" title="Letters are colored as in Clustalx and Jalview, with colors depending on composition of the column.">' +
        '<span aria-hidden="true" data-icon="?"></span><span class="reader-text">help</span></a>';
    }

    var color_controls = '<fieldset><legend>Color Scheme</legend>' +
      '<label><input type="radio" name="color" class="logo_color" value="default" ' + def_color +
      '/>Default ' + def_help +
      '</label></br>' +
      '<label><input type="radio" name="color" class="logo_color" value="consensus" ' + con_color +
      '/>Consensus Colors ' + con_help +
      '</label>' +
      '</fieldset>';
    settings.append(color_controls);
  }


  if (logo.data.ali_map) {
    var mod_checked = null,
    ali_checked = null,
    mod_help = '',
    ali_help = '';

    if (logo.display_ali_map === 0) {
      mod_checked = 'checked';
    } else {
      ali_checked = 'checked';
    }

    if (options.help) {
      mod_help = '<a class="help" href="/help#coords_model" title="The coordinates along the top of the plot show the model position.">' +
        '<span aria-hidden="true" data-icon="?"></span><span class="reader-text">help</span></a>';
      ali_help = '<a class="help" href="/help#coords_ali" title="The coordinates along the top of the plot show the column in the alignment associated with the model">' +
        '<span aria-hidden="true" data-icon="?"></span><span class="reader-text">help</span></a>';
    }

    var ali_controls = '<fieldset><legend>Coordinates</legend>' +
      '<label><input type="radio" name="coords" class="logo_ali_map" value="model" ' + mod_checked +
      '/>Model ' + mod_help +
      '</label></br>' +
      '<label><input type="radio" name="coords" class="logo_ali_map" value="alignment" ' + ali_checked +
      '/>Alignment ' + ali_help +
      '</label>' +
      '</fieldset>';
    settings.append(ali_controls);
  }


  var controls = $('<div class="logo_controls"></div>');
  if (logo.zoom_enabled) {
    controls.append('<button class="logo_zoomout button">-</button>' +
                    '<button class="logo_zoomin button">+</button>');
  }

  if (settings.children().length > 0) {
    controls.append('<button class="logo_settings_switch button">Settings</button>');
    controls.append(settings);
  }

  form.append(controls);

  return form;
}
