from flask import Flask, request, jsonify
import xml.etree.ElementTree as ET
import requests

app = Flask(__name__)

@app.route("/convert", methods=["GET"])
def convert():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "Missing 'url' query parameter."}), 400

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500

    try:
        root = ET.fromstring(response.text)
        markdown_list = []

        for i, item in enumerate(root.findall(".//item")):
            if i >= 1000:
                break
            title = item.findtext("title", "No title")
            description = item.findtext("description", "No description")
            link = item.findtext("link", "#")
            price = item.findtext("price", "N/A")

            markdown = f"""## {title}\n\n**Price:** {price}  \n**Description:** {description}  \n[View Product]({link})\n\n---\n"""
            markdown_list.append(markdown)

        output = "\n".join(markdown_list)
        return jsonify({"markdown": output})

    except ET.ParseError:
        return jsonify({"error": "Failed to parse XML."}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
