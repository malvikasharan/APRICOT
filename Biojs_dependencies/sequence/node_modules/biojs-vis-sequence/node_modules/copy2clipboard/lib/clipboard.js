var defer = require("./defer");

var Clipboard = function Clipboard() {
  this.value = "";
  var self = this;

  var area = document.createElement("textarea");
  area.id = "clipboard";
  area.style.display = "none";
  area.style.width = "1px";
  area.style.height = "1px";

  var container = document.createElement("div");
  container.style.position = "absolute";
  container.style.top = "-100px";
  area.style.width = "0px";
  area.style.height = "0px";
  container.id = "clipboard-container";
  container.appendChild(area);

  // TODO: check for multiple
  document.body.appendChild(container);

  document.addEventListener("keydown", function(e) {
    // only activate the clipboard if there is text and someone wants to copy
    if (!self.value || !(e.ctrlKey || e.metaKey)) {
      return;
    }
    // there is some other text that they want to 
    var tagName = e.target.tagName;
    if (tagName === "input" || tagName === "textarea") {
      return;
    }
    
    // check for user selections
    var windowSel;
    if (typeof window.getSelection === "function" ? (windowSel = window.getSelection()) != null ? windowSel.toString() : false : false) {
      return;
    }
    
    // check for user selections
    var documentSel;
    if ((documentSel = document.selection) != null ? documentSel.createRange().text : false) {
      return;
    }
    defer(function() {
      container.style.display = "block";
      area.textContent = self.value;
      area.style.display = "block";
      area.focus();
      area.select();
    });
  });
  document.addEventListener("keyup", function(e) {
    // inactive the clipboard
    if (e.target.id === "clipboard") {
      if (!(e.ctrlKey || e.metaKey)) {
        container.style.display = "none";
        area.textContent = "";
      }
    }
  });
};

Clipboard.prototype.set = function(value) {
  this.value = value;
};

module.exports = Clipboard;
