// IndexedDB（簡易版）で未送信データを保存
const dbName = "InputDataDB";
const storeName = "inputData";
// IndexedDBセットアップ
function openDB() {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open(dbName, 1);
    request.onupgradeneeded = (event) => {
      event.target.result.createObjectStore(storeName, { autoIncrement: true });
    };
    request.onsuccess = () => resolve(request.result);
    request.onerror = () => reject(request.error);
  });
}

// IndexedDBにデータを保存し、保存されたデータのキーを返す
function saveDataLocally(data) { 
  return openDB().then(db => {
    const tx = db.transaction(storeName, "readwrite");
    const store = tx.objectStore(storeName);
    const request = store.add({ data, sent: false });
    request.onsuccess = (event) => console.log("Data saved with key:", event.target.result); // デバッグ用
    return tx.complete;
  });
}
function getUnsyncedData() {
  return openDB().then(db => {
    return new Promise((resolve) => {
      const tx = db.transaction(storeName, "readonly");
      const store = tx.objectStore(storeName);
      const itemsWithKeys = [];
      store.openCursor().onsuccess = (event) => {
        const cursor = event.target.result;
        if (cursor) {
          if (!cursor.value.sent) {
            itemsWithKeys.push({ id: cursor.key, data: cursor.value.data });
          }
          cursor.continue();
        } else {
          resolve(itemsWithKeys);
        }
      };
    });
  });
}
function markDataAsSent(id) {
  return openDB().then(db => {
    const tx = db.transaction(storeName, "readwrite");
    const store = tx.objectStore(storeName);
    const req = store.get(id);
    req.onsuccess = () => {
      const item = req.result;
      if (item) {
        item.sent = true; // sent フラグを true に設定
        store.put(item, id);
      }
    };
    return tx.complete;
  });
}
// サーバー送信
function sendDataToServer(data) {
  return fetch('/api/input', {
    method: 'POST',
    body: JSON.stringify(data),
    headers: {'Content-Type': 'application/json'}
  });
}
// 送信処理
function trySendLocalData() {
  getUnsyncedData().then(items => {
    items.forEach(item => { // item は { id: key, data: {name, action} } の形式
      sendDataToServer(item.data) // item.data は {name, action}
        .then(() => markDataAsSent(item.id)) // IndexedDB のキーを渡す
        .catch(() => {}); // 失敗時はそのまま
    });
  });
}


document.getElementById('enterBtn').addEventListener('click', () => {
  console.log("発火")
    handleSubmit("入室");
});

document.getElementById('exitBtn').addEventListener('click', () => {
    handleSubmit("退室");
});

function handleSubmit(action) {
    const input = document.getElementById('dataInput').value;

    if (navigator.onLine) {
        sendDataToServer({name: input, action: action})
            .then(() => {
                document.getElementById('status').innerText = '送信成功（オンライン）';
            })
            .catch(() => {
                saveDataLocally({name: input, action: action});
                document.getElementById('status').innerText = '送信失敗→ローカル保存';
            });
    } else {
        saveDataLocally({name: input, action: action});
        document.getElementById('status').innerText = 'オフライン→ローカル保存';
    }
}


// ネット復旧時に未送信データ送信
window.addEventListener('online', trySendLocalData);