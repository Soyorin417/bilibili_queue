from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)  # 允许所有来源

config_path = os.path.join(os.path.dirname(__file__), "config.json")

# -------- 配置接口 --------
@app.get("/config")
def get_config():
    with open(config_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return jsonify(data)

@app.post("/config")
def save_config():
    data = request.json
    print("收到前端数据:", data)
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return jsonify({"status": "ok"})

# -------- 队列接口 --------
@app.get("/queue")
def get_queue():
    queue_path = os.path.join(os.path.dirname(__file__), "queue.json")
    if not os.path.exists(queue_path):
        return jsonify([])  # 文件不存在，返回空列表
    return send_file(queue_path, mimetype="application/json")

@app.post("/queue/remove")
def remove_from_queue():
    data = request.json
    uid_to_remove = data.get("uid")
    if uid_to_remove is None:
        return jsonify({"status": "error", "msg": "缺少 uid"}), 400

    if not os.path.exists(queue_path):
        return jsonify({"status": "error", "msg": "队列不存在"}), 404

    with open(queue_path, "r", encoding="utf-8") as f:
        queue = json.load(f)

    # 根据 uid 过滤
    new_queue = [u for u in queue if u.get("uid") != uid_to_remove]

    with open(queue_path, "w", encoding="utf-8") as f:
        json.dump(new_queue, f, ensure_ascii=False, indent=2)

    print(f"用户 uid={uid_to_remove} 已退队")
    return jsonify({"status": "ok", "queue": new_queue})


# -------- 队列接口：更新队列 --------
@app.post("/queue")
def save_queue():
    queue_path = os.path.join(os.path.dirname(__file__), "queue.json")
    data = request.json
    print("收到队列更新:", data)
    with open(queue_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return jsonify({"status": "ok"})
# -------- 获取关键词 --------
@app.get("/keywords")
def get_keywords():
    with open(config_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return {
        "join_words": data.get("join_words", []),
        "pop_words": data.get("pop_words", [])
    }

# -------- 保存关键词 --------
@app.post("/keywords")
def save_keywords():
    data = request.json
    join_words = data.get("join_words", [])
    pop_words = data.get("pop_words", [])

    # 读取原 config
    with open(config_path, "r", encoding="utf-8") as f:
        config_data = json.load(f)

    # 更新关键词
    config_data["join_words"] = join_words
    config_data["pop_words"] = pop_words

    # 写回 config.json
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config_data, f, ensure_ascii=False, indent=2)

    print("关键词已更新:", config_data)
    return jsonify({"status": "ok"})

# -------- 启动服务器 --------
if __name__ == "__main__":
    app.run(port=5000)
