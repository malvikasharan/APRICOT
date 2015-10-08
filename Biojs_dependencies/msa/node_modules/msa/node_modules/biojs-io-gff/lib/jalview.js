var jalview = {};
module.exports = jalview;
var utils = require("./utils");

// http://www.jalview.org/help/html/features/featuresFormat.html
jalview.readHeader = function(lines) {
  var colors = {};
  var i = 0;
  var features = [];
  var currentGroup;

  for (; i < lines.length; i++) {
    var line = lines[i];
    if (line.indexOf("#") >= 0) {
      // no comments allowed -> stop
      break;
    }
    var columns = line.split(/\t/);
    var firstCell = columns[0].trim();
    if (firstCell === "GFF") {
      // this symbolizes the end 
      break;
    } else if (columns.length === 2) {
      if (firstCell === "startgroup") {
        currentGroup = columns[1].trim();
      } else if (firstCell === "endgroup") {
        currentGroup = "";
        continue;
      } else {
        // parse color
        colors[columns[0]] = jalview.parseColor(columns[1]);
      }
    } else if(columns.length >= 5){
      var arr = jalview.parseLine(columns);
      if (currentGroup) {
        arr.attributes.Parent = currentGroup;
      }
      features.push(arr);
    }
  }

  return {
    offset: i,
    colors: colors,
    features: features
  };
};

jalview.parseColor = function(cell) {
  if (cell.indexOf(",") >= 0) {
    // rgb code
    return utils.rgbToHex(cell.split(",").map(function(el) {
      return parseInt(el);
    }));
  }
  // color names with length == 6
  // 'bisque,maroon,orange,orchid,purple,salmon,sienna,tomato,violet,yellow'
  if (cell.length === 6 && parseInt(cell.charAt(0), 16) <= 16 && cell !== 'bisque') {
    // hex code
    return "#" + cell;
  }
  // color name
  return cell;
};


jalview.parseLine = function(columns) {
  var obj = {
    attributes: {}
  };
  obj.attributes.Name = columns[0].trim(); //desc
  obj.seqname = columns[1].trim(); // id
  obj.start = parseInt(columns[3]);
  obj.end = parseInt(columns[4]);
  obj.feature = columns[5].trim();
  if (obj.seqname === "ID_NOT_SPECIFIED") {
    obj.seqname = columns[2].trim(); // alternative id
  }
  return obj;
};
