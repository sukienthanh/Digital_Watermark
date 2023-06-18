from flask import Flask, render_template,jsonify, request
import watermark
import uploadImage

app = Flask(__name__)

@app.route("/watermarking")
def index():   
   return render_template("index.html")

@app.route('/')
@app.route("/welcome")
def welcome():    
   return render_template("welcome.html")


@app.route("/Extract", methods=['POST'])
def Extract():
   alpha = request.form["alpha"]
   coverName = request.form["watermarked"]
   wmName = request.form["wmName"]
   ncc = watermark.extract(coverName,wmName,alpha)   
   return jsonify(ncc)


@app.route("/ExtractAttacked", methods=['POST'])
def ExtractAttacked():
   method = request.form["method"]
   alpha = request.form["alpha"]
   coverName = request.form["watermarked"]
   wmName = request.form["wmName"]
   ncc = watermark.extract_after_attacked(coverName,wmName, method, alpha)  
   return jsonify(ncc)


@app.route("/Embed", methods=['POST'])
def Embed():
   coverName = request.form["coverName"]
   wmName = request.form["wmName"]
   alpha = request.form["alpha"]
   psnr = watermark.embed(coverName,wmName,alpha)   
   return jsonify(psnr)


@app.route("/Attack", methods=['POST'])
def Attack():
   percent = request.form["percent"]
   attackMethod = request.form["attackMethod"]
   watermarked = request.form["watermarked"]
   psnr = watermark.attackImage(attackMethod,watermarked, percent)
   
   return jsonify(psnr)


@app.route("/UploadCover", methods=['POST'])
def UploadCover():
   fileUpload = request.files.get('image')    
   path = 'venv/static/cover/' 
   fileUpload.save(path + fileUpload.filename)
   uploadImage.getGrayLayer(fileUpload.filename)
   return jsonify(fileUpload.filename)


@app.route("/UploadWatermark", methods=['POST'])
def UploadWatermark():
   coverImage = request.form["coverImage"]
   fileUpload = request.files.get('image')    
   path = 'venv/static/watermark/' 
   fileUpload.save(path + fileUpload.filename)  
   return jsonify(fileUpload.filename)


if __name__ == '__main__':
   app.run(debug = True)



   