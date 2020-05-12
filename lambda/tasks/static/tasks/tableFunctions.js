function sortTable(tableId, col, type) {
  let table = document.getElementById(tableId);
  let rows = table.rows;

  let sort_count = 0;
  let sorting =true;

  while (sorting) {
    sorting = false;

    for (let i = 1; i < rows.length-1; i++) {
      let swap = false;
      let x = rows[i].querySelectorAll("th, td")[col]
      let y = rows[i + 1].querySelectorAll("th, td")[col]

      if (x.dataset.sortValue) {
        x = x.dataset.sortValue
        y = y.dataset.sortValue
      } else {
        x = x.innerHTML;
        y = y.innerHTML;
      }

      if (type === "number") {
        x = Number(x);
        y = Number(y);
      }

      if (x > y) {
        swap = true;
      }

      if (swap) {
        rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
        sorting = true;
        sort_count++;
      }
    }
  }
}

function reverseTable(tableId) {
  table = document.getElementById(tableId);
  rows = table.rows;
  last_row = rows.length - 1;

  for (let i = 1; i < rows.length; i++) {
    rows[i].parentNode.insertBefore(rows[last_row], rows[i]);
  }
}


const sortHeaders = document.getElementsByClassName("sortHeader");

Array.from(sortHeaders).forEach(header => {
  header.addEventListener('click', (event) => {
      const target = event.target;
      const sorted = (target.dataset.sorted === 'true');
      if (sorted) {
        reverseTable(target.dataset.tableId);
      } else {
        const tableId = target.dataset.tableId;
        const tableHeaders = document.getElementById(tableId).getElementsByClassName("sortHeader")
        Array.from(tableHeaders).forEach( header2 => {
          header2.dataset.sorted = false;
        })
        sortTable(tableId, target.dataset.col, target.dataset.type);
        target.dataset.sorted = true;
      }
  })
})
