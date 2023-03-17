// #region fetch the core modules //
var modules = {};
async function load() {
  return await fetch("./static/assets/html/modules.html")
    .then(function (response) {
      return response.text();
    })
    .then(function (html) {
      let parser = new DOMParser();
      return parser.parseFromString(html, "text/html");
    })
    .catch(function (err) {
      console.log("Failed to fetch the addons modules: ", err);
      return;
    });
}
async function load1() {
  let a = await fetch("./static/assets/html/modules.html");
  let b = await a.text();
  let parser = new DOMParser();
  let c = parser.parseFromString(b, "text/html");
  return c;
}
async function caller() {
  modules["addons"] = await load1();
  startModule();
}
caller();

// var tags = Array.prototype.slice
//   .call(modules["addons"]["head"].getElementsByTagName("script"))
//   .concat(
//     Array.prototype.slice.call(
//       modules["addons"]["head"].getElementsByTagName("link")
//     )
//   );
// tags.forEach((element) => {
//   var tag = document.createElement(element.nodeName);
//   tag.onload = () => {
//     console.log(element.name, " loaded successfuly");
//   };
//   Array.prototype.forEach.call(element.attributes, (element) => {
//     tag.setAttribute(element.name, element.textContent);source
//   });
//   // tag.setAttribute("async", false);
//   // tag.defer = true;
//   document.head.appendChild(tag);
//   //eval(tag.outerHTML);
// });
// #endregion fetch the core modules //

var moduleInfo = {};

function startModule() {
  moduleManage().loadModules([
    { core: "addons", name: "sankeychart" },
    { core: "addons", name: "forcechart" },
    { core: "addons", name: "chart1-container" },
  ]);

  // #region add-ons loading //
  function moduleManage() {
    const load = (module) => {
      module = { ...module, ...{ script: "", method: {}, event: {} } };
      let src = modules[module.core].getElementById(module.name + "-container");
      let des = document.getElementById(module.name + "-container");
      des.innerHTML = src.innerHTML;
      if (des.querySelector("script") != undefined)
        eval("module.script = " + des.querySelector("script").innerHTML.trim());
      return module;
    };
    const loadModule = (module) => {
      if (moduleInfo[module.name] == undefined) {
        module = load(module);
        module.init = eval("moduleHandle_" + module.name);
        module.method = module.script(); //();
        moduleInfo[module.name] = {
          core: module.core,
          name: module.name,
          script: module.script,
          method: module.method.method,
          init: module.init,
        };
        module.ret = module.init();
        moduleInfo[module.name].method.setCallback(module.ret.event);
        moduleInfo[module.name].event = module.ret.event;
      } else {
        module = moduleInfo[module.name];
        module.ret = module.init();
      }
    };
    const unloadModule = (moduleName) => {
      let des = document.getElementById(moduleName + "-container");
      des.innerHTML = "";
      delete moduleInfo[moduleName];
    };
    return {
      loadModules: function (moduleList) {
        moduleList.forEach((module) => loadModule(module));
      },
      loadModule: loadModule,
      unloadModuleAll: function () {
        Object.keys(moduleInfo).forEach((moduleName) =>
          unloadModule(moduleName)
        );
      },
      unloadModule: unloadModule,
    };
  }
  function visibility() {
    return {
      hideForm: function (form) {
        document.getElementById(form + "-container").style.display = "none";
      },
      showForm: function (form) {
        let node = document.getElementById(form + "-container");
        while (node.tagName != "BODY") {
          node.style.display = "block";
          node = node.parentElement;
        }
      },
      hideShow: function (forms) {
        forms.hide.forEach((form) => {
          document.getElementById(form + "-container").style.display = "none";
        });
        forms.show.forEach((form) => {
          let node = document.getElementById(form + "-container");
          while (node.tagName != "BODY") {
            node.style.display = "block";
            node = node.parentElement;
          }
        });
      },
    };
  }

  // #endregion add-ons loading //

  // #region add-ons/modules handling //
  function moduleHandle_sankeychart() {
    init();

    function init() {
      moduleInfo.sankeychart.method.init();
    }

    return {
      init: function () {
        init();
      },
      event: function (arg) {
        switch (arg.action) {
          case "event1":
            break;
          case "event2":
            break;
        }
      },
    };
  }
  function moduleHandle_forcechart() {
    init();

    function init() {
      moduleInfo.forcechart.method.init();
    }

    return {
      init: function () {
        init();
      },
      event: function (arg) {
        switch (arg.action) {
          case "event1":
            break;
          case "event2":
            break;
        }
      },
    };
  }
  function moduleHandle_chart1() {
    init();

    function init() {
      moduleInfo.chart1.method.init();
    }

    return {
      init: function () {
        init();
      },
      event: function (arg) {
        switch (arg.action) {
          case "event1":
            break;
          case "event2":
            break;
        }
      },
    };
  }
  // #endregion add-ons/modules handling //
}
