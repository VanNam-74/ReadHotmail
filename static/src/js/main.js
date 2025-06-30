function logoutEvent() {
  fetch("{{ url_for('logout__action') }}", {
    method: "POST",
    data: "",
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.logout == "success") {
        window.location.href = "/login__action";
      }
    });
}

document
  .getElementById("fileInput")
  .addEventListener("change", async function (event) {
    const file = event.target.files[0];
    if (file) {
      const formData = new FormData();
      formData.append("file", file);

      try {
        const response = await fetch("import_profile__action", {
          method: "POST",
          body: formData,
        });


        if (!response.ok) {
          const text = await response.text();
          throw new Error(text);
        }
        const result = await response.json();
        const totalPages = result.total;
        const page = result.page;
        const limit = result.limit;
        const data = result.data;


        renderTable(data);
        enableButton();
        renderPaginate(totalPages, page, limit)
      } catch (error) {
        console.error("Lỗi khi upload:", error);
      }
      event.target.value = "";
    }
  });
function renderPaginate(total, page, limit) {
  const pages = Math.ceil(total / limit);
  const current = page;
  let html = '';
  for (let i = 1; i <= pages; i++) {
    html += `<li><button onclick="fetchPage(${total},${i}, ${limit})" ${i === current ? 'disabled' : ''}>${i}</button></li>`;
  }

  document.getElementById("panigate_page").innerHTML = `<ul>${html}</ul>`;

  currentPageData = { total, page, limit };
  updatePageInfo();
}

async function fetchPage(total, page, limit) {
  try {
    const response = await fetch(`paginate_page/${page}?total=${total}&limit=${limit}`, {
      method: "GET",
    })

    if (!response.ok) {
      const text = await response.text();
      throw new Error(text);
    }

    const result = await response.json()
    const data = result.result
    setTimeout(() => {
      renderPaginate(total, page, limit);
      renderTable(data);
      window.addEventListener('load', () => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
      });
    }, 100);

  } catch (error) {

  }
}


function updatePageInfo() {
  const pages = Math.ceil(currentPageData.total / currentPageData.limit);
  const info = `Trang ${currentPageData.page}/${pages} - Hiển thị ${currentPageData.limit} items/trang - Tổng: ${currentPageData.total} items`;
  document.getElementById("page-info").textContent = info;
}


function renderTable(data) {
  const html = data.map(row => `
                <tr class="{{ loop.index0 }}">
                    <td id="idProfile" class="id">${row["Profile_id"]}</td>
                    <td>${row["Profile_name"]}</td>
                    <td>${row["Browser"]}</td>
                    <td>Http| ${row["Proxy_ip"]}:${row["Proxy_port"]}</td>
                    <td>${row["Access_token"]}</td>
                    <td>${row["Status"]}</td>
                    <td>
                        <div class="action-column">
                            <div class="item-button start-button disabled" data-id="${row['ID']}" onclick="start_action_event(this)">
                                <img src="/static/publish/plus.png" alt="" style="max-width:12px">
                                <span>Start</span>
                            </div>
                        </div>
                    </td>
                </tr>
                
        `).join("");

  document.getElementById("table").innerHTML =
    `
          <table>
          <thead>
                <tr>
                    <th>ID</th>
                    <th>Profile name</th>
                    <th>Browser</th>
                    <th>Proxy</th>
                    <th>Token</th>
                    <th>Status</th>
                    <th>Action</th>
                </tr>
            </thead>
            <tbody id="table-body">
           ${html}
          </tbody>
          </table>
          
          `;
}


function enableButton() {
  const data = getDataTableProfile();
  const getTokenButton = document.querySelector(".getToken-button");
  getTokenButton.classList.remove("disabled");
}
function getDataTableProfile() {
  const table = document.getElementById("table");
  const rows = table.querySelectorAll("tbody tr");
  const data = [];

  rows.forEach((row) => {
    const cells = row.querySelectorAll("td");
    const rowData = Array.from(cells).map((cell) => cell.textContent.trim());
    data.push(rowData);
  });

  return data;
}
async function getTokenEvent() {
  const profileCount = document.querySelectorAll("tbody tr").length;
  const idProfileArray = Array.from(document.querySelectorAll(".id")).map(
    (id) => id.textContent.trim()
  );
  try {
    const response = await fetch("get_token__action", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        profileCount: profileCount,
      }),
    });

    const data = await response.json();
    if (data.status_code === 200) {
      actionArray = data.data;
      const start_action_ele_array = document.querySelectorAll(".start-button");
      for (const actionItem of actionArray) {
        if (actionItem["action"] === "start") {
          start_action_ele_array[actionItem["position"]].classList.remove(
            "disabled"
          );
        }
      }
    } else {
      console.error("Lỗi khi lấy token:", data.message);
    }
  } catch (error) {
    console.error("Lỗi khi lưu idProfileArray vào localStorage:", error);
  }
}
function animateDots(span) {
  let dotCount = 0;
  return setInterval(() => {
    dotCount = (dotCount + 1) % 16; //0-10
    span.textContent = ".".repeat(dotCount);
  }, 500);
}
async function start_action_event(element) {
  const profileID = element.getAttribute("data-id");
  const startElement = element.querySelector("span");
  const imageElement = element.querySelector("img");
  // let readButton = document.querySelector(
  //   `.read-button[data-id="${profileID}"]`
  // );

  const loadingInterval = animateDots(startElement);
  element.classList.add("starting");
  imageElement.style.display = "none";

  if (profileID != null) {
    ID = profileID;
  } else {
    ID = "null";
  }
  var response = await fetch("start__action", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      id_profile: ID,
    }),
  })
  const data = await response.json();
  result = data.is_stop;
  if (result) {
    clearInterval(loadingInterval);
    imageElement.style.display = "block";
    startElement.innerHTML = "Start";
  }

  // .then((response) => response.json)
  // .then((value) => {
  //   data = value.success;
  //   if (!data) {
  //     clearInterval(loadingInterval);
  //     imageElement.style.display = "block";
  //     startElement.innerHTML = "Start";
  //     // readButton.classList.remove("disabled");
  //   } else {
  //     document.getElementById("table").innerHTML = "Fail";
  //   }
  // });
}
