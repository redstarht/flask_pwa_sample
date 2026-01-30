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
function saveDataLocally(data) {
  return openDB().then(db => {
    const tx = db.transaction(storeName, "readwrite");
    tx.objectStore(storeName).add({ data, sent: false });
    return tx.complete;
  });
}
function getUnsyncedData() {
  return openDB().then(db => {
    return new Promise((resolve) => {
      const tx = db.transaction(storeName, "readonly");
      const store = tx.objectStore(storeName);
      const req = store.getAll();
      req.onsuccess = () => resolve(req.result.filter(item => !item.sent));
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
        item.sent = true;
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
    items.forEach((item, idx) => {
      sendDataToServer(item.data)
        .then(() => markDataAsSent(idx))
        .catch(() => {}); // 失敗時はそのまま
    });
  });
}
// 入力フォーム処理
document.getElementById('inputForm').addEventListener('submit', function(e) {
  e.preventDefault();
  const input = document.getElementById('dataInput').value;
  if (navigator.onLine) {
    sendDataToServer({data: input})
      .then(() => {
        document.getElementById('status').innerText = '送信成功（オンライン）';
      })
      .catch(() => {
        saveDataLocally(input);
        document.getElementById('status').innerText = '送信失敗→ローカル保存';
      });
  } else {
    saveDataLocally(input);
    document.getElementById('status').innerText = 'オフライン→ローカル保存';
  }
});
// ネット復旧時に未送信データ送信
window.addEventListener('online', trySendLocalData);