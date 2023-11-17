from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import cv2
from backend_weather_iot.base_view import BaseView
import numpy as np
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
import json
import os
from tensorflow.keras.preprocessing.image import load_img

model = load_model('C:/Users/ADMIN/Desktop/Hoc/This semester/IoT/weather_iot/backend-iot/model.h5')

# Create your views here.
class DiseaseDetection(BaseView):
    def post(self, request: HttpRequest):
        # todo authentication
        image = request.FILES['image']
        filename = image.name
        print("@@ Input posted = ", filename)

        file_path = os.path.join(
            "C:/Users/ADMIN/Desktop/Hoc/This semester/IoT/weather_iot/backend-iot/upload/",
            filename,
        )
        with open(file_path, 'wb') as destination:
            for chunk in image.chunks():
                destination.write(chunk)

        print("@@ Predicting class......")
        test_image = load_img(file_path, target_size=(128, 128))  # load image
        print("@@ Got Image for prediction")
        test_image = (
            img_to_array(test_image) / 255
        )  # convert image to np array and normalize
        test_image = np.expand_dims(test_image, axis=0)  # change dimention 3D to 4D

        result = model.predict(test_image)  # predict diseased plant or not
        print("@@ Raw result = ", result)

        pred = np.argmax(result, axis=1)
        print(pred)
        if pred == 0:
            res = json.dumps({
                "tree": "Táo",
                "disease": "Bệnh ghẻ trên cây táo (Apple Scab Disease)",
                "treatment": "Giữ cho môi trường xung quanh cây trồng sạch sẽ bằng cách loại bỏ cỏ dại, mảnh vụn thực vật, các bộ phận của cây bị thiệt hại, phát triển của các loại cây không mong muốn và các thực vật xung quanh tự mọc và không được bảo vệ."
            })
            return HttpResponse(res, content_type='application/json', status=200)
        elif pred == 1:
            res = json.dumps({
                "tree": "Táo",
                "disease": "Bệnh thối đen (Apple Black Rot)",
                "treatment": "Xử lý bệnh thối đen trên cây táo bắt đầu bằng công tác vệ sinh. Vì bào tử nấm mùa đông trên lá rụng, trái cây ướp xác, vỏ cây chết và vỏ hộp , nên điều quan trọng là phải dọn sạch tất cả các mảnh vụn rơi và trái cây chết và tránh xa cây."
            })
            return HttpResponse(res, content_type='application/json', status=200)
        elif pred == 2:
            res = json.dumps({
                "tree": "Táo",
                "disease": "Bệnh gỉ sắt táo (Cedar Apple Rust)",
                "treatment": "Táo bị bệnh gỉ sắt táo cần được chăm sóc đặc biệt để khắc phục bệnh mà vẫn sinh quả. Đầu tiên, hãy kiểm tra xem bạn có loài cây bách xù nào gần cây táo của bạn không. Nếu chúng bị nhiễm bệnh, chúng sẽ tạo ra những vết thương vào mùa xuân và mùa hè có thể phát triển khá lớn. Chúng tạo ra những đường gân màu cam đặc biệt khó bỏ lỡ. Các bào tử từ chúng có thể lây nhiễm bất kỳ cây táo nào gần đó.\nMột cách để kiểm soát căn bệnh này là loại bỏ hoặc tiêu diệt bất kỳ cây bách nào gần đó. Hoặc bạn chỉ có thể theo dõi chúng để tìm kiếm và phá hủy cây hoặc cắt tỉa và phá hủy các nhánh bằng các lỗ hổng. Một cách khác để kiểm soát bệnh gỉ sắt táo là trồng các giống táo có khả năng chống nhiễm trùng: Red Delicious, McIntosh, Wineap, Empire, và các loại khác.\nMột bình xịt thuốc diệt nấm cũng có thể được sử dụng. Vườn ươm địa phương của bạn có thể giúp bạn tìm thấy bình xịt thích hợp. Tuy nhiên, phòng ngừa thường là một cách tốt hơn để kiểm soát bệnh này trên cây táo. Khoảng 1.000 feet giữa táo và các loài cây bách xù là đủ để bảo vệ cây của bạn. Ngoài ra, hãy nhớ rằng mức độ nhiễm trùng thấp sẽ không ảnh hưởng đến cây trồng của bạn rất nhiều."
            })
            return HttpResponse(res, content_type='application/json', status=200)
        elif pred == 3:
            res = json.dumps({
                "tree": "Táo",
                "disease": "Không có bệnh",
                "treatment": "Không có bệnh"
            })
            return HttpResponse(res, content_type='application/json', status=200)
        elif pred == 4:
            res = json.dumps({
                "tree": "Ảnh nền",
                "disease": "Ảnh nền không chứa lá cây",
                "treatment": "Hãy đảm bảo rằng bạn đã chụp đúng ảnh lá cây, và chụp cận cảnh 1 chiếc lá"
            })
            return HttpResponse(res, content_type='application/json', status=200)
        elif pred == 5:
            res = json.dumps({
                "tree": "Ngô",
                "disease": "Đốm lá Cercospora/Đốm lá xám (Cercospora Leaf Spot/Gray Leaf Spot)",
                "treatment": "Để kiểm soát bệnh đốm lá ngô, có thể áp dụng các biện pháp như sử dụng giống ngô chống chịu bệnh, quản lý cân bằng độ ẩm trong vườn, tránh gieo cấy quá sát nhau, thực hiện xoá bỏ và tiêu hủy những phần cây bị nhiễm bệnh, và sử dụng thuốc trừ sâu hoặc thuốc bảo vệ thực vật phù hợp nếu cần thiết."
            })
            return HttpResponse(res, content_type='application/json', status=200)
        elif pred == 6:
            res = json.dumps({
                "tree": "Ngô",
                "disease": "Bệnh gỉ sắt thường gặp trên ngô (Common Rust)",
                "treatment": "Biện pháp quản lý tốt nhất là sử dụng các giống ngô lai kháng bệnh. Thuốc diệt nấm cũng có thể có lợi, đặc biệt nếu áp dụng sớm khi đã xuất hiện ít mụn mủ trên lá."
            })
            return HttpResponse(res, content_type='application/json', status=200)
        elif pred == 8:
            res = json.dumps({
                "tree": "Ngô",
                "disease": "Không có bệnh",
                "treatment": "Không có bệnh"
            })
            return HttpResponse(res, content_type='application/json', status=200)
        elif pred == 7:
            res = json.dumps({
                "tree": "Ngô",
                "disease": "Bệnh bạc lá nghệ trên ngô (Northern Leaf Blight)",
                "treatment": "Sử dụng giống lai kháng bệnh. Thuốc diệt nấm có thể được sử dụng trên các giống cận huyết để sản xuất hạt giống trong giai đoạn đầu của bệnh này. Các biện pháp luân canh và làm đất có thể hữu ích trong một số trường hợp."
            })
            return HttpResponse(res, content_type='application/json', status=200)
        elif pred == 9:
            res = json.dumps({
                "tree": "Nho",
                "disease": "Bệnh thối đen (Grape Black Rot)",
                "treatment": "Những cành cắt tỉa và quả ướp xác bị nhiễm bệnh phải được loại bỏ, đốt và/hoặc chôn trong đất trước khi cây mới bắt đầu phát triển vào mùa xuân. Ở những vườn nho có các giống mẫn cảm hoặc nơi bệnh thối đen đã xảy ra vào năm trước, nên phun thuốc diệt nấm vào đầu mùa để ngăn ngừa nhiễm trùng sớm nhất. Nếu nhiễm trùng trở nên nhiều, việc bảo vệ chống thối quả là rất khó khăn vào cuối mùa sinh trưởng. Khuyến khích trồng các giống kháng bệnh."
            })
            return HttpResponse(res, content_type='application/json', status=200)
        elif pred == 10:
            res = json.dumps({
                "tree": "Nho",
                "disease": "Sởi đen (Esca/Black Measles)",
                "treatment": "Hiện nay, chưa có chiến lược quản lý hiệu quả bệnh sởi. Những người trồng nho làm rượu vang với những vườn nho nhỏ thường yêu cầu nhân viên hiện trường loại bỏ những quả bị nhiễm bệnh trước khi thu hoạch. Nho khô bị bệnh sởi sẽ bị loại bỏ trong quá trình thu hoạch hoặc tại nhà đóng gói, trong khi người trồng nho sẽ để lại quả bị bệnh trên cây nho. Nghiên cứu hiện tại tập trung vào việc bảo vệ các vết cắt tỉa khỏi bị nhiễm nấm để giảm thiểu nấm nghi ngờ xâm nhập vào vết thương mới."
            })
            return HttpResponse(res, content_type='application/json', status=200)
        elif pred == 12:
            res = json.dumps({
                "tree": "Nho",
                "disease": "Không có bệnh",
                "treatment": "Không có bệnh"
            })
            return HttpResponse(res, content_type='application/json', status=200)
        elif pred == 11:
            res = json.dumps({
                "tree": "Nho",
                "disease": "Bệnh bạc lá/Đốm lá Isariopsis (Leaf Blight/Isariopsis Leaf Spot)",
                "treatment": "Để kiểm soát bệnh bạc lá, hãy cắt tỉa và tiêu hủy những cành bị nhiễm bệnh. Nếu bệnh bạc lá đã xuất hiện trong vườn nho của bạn, hãy phun thuốc diệt nấm vào mùa xuân và mùa hè. Hãy nhớ rằng thuốc diệt nấm có thể gây hại cho môi trường, vì vậy hãy đọc nhãn trước khi sử dụng. Nếu bạn không muốn sử dụng thuốc diệt nấm, hãy chọn các giống nho kháng bệnh."
            })
            return HttpResponse(res, content_type='application/json', status=200)
        elif pred == 13:
            res = json.dumps({
                "tree": "Khoai tây",
                "disease": "Bệnh bạc lá sớm (Early Blight)",
                "treatment": "Trong nhiều trường hợp, áp dụng các biện pháp canh tác hợp lý để duy trì sức khỏe tốt cho cây khoai tây và cà chua sẽ giữ cho tổn thất do bệnh bạc lá sớm ở mức thấp hơn mức kinh tế. Bởi vì mầm bệnh qua mùa đông trên tàn dư cây trồng bị nhiễm bệnh nên các quy trình vệ sinh tại đồng ruộng giúp giảm lượng vi khuẩn lây nhiễm ban đầu ở các vụ tiếp theo là có lợi. Cần cân nhắc việc loại bỏ các vật liệu có khả năng bị nhiễm bệnh như dây leo và trái cây mục nát khỏi vùng lân cận ruộng sản xuất. Kiểm soát các loài cỏ dại và cỏ dại, chẳng hạn như cây cà ri và cây tầm ma, vốn là vật chủ thay thế cho bệnh, trước khi trồng cây trồng mới sẽ giúp giảm nguy cơ lây truyền bệnh. Đảm bảo hạt giống hoặc cây cấy không có mầm bệnh trước khi đưa ra đồng ruộng và luân canh ruộng sang cây ký chủ không nhạy cảm cũng sẽ giúp giảm sự tích tụ vật liệu cấy trong đất. Độ trưởng thành tối ưu của củ là yếu tố quan trọng nhất để kiểm soát nhiễm trùng củ. Củ thu hoạch trước khi trưởng thành dễ bị tổn thương và nhiễm trùng. Có thể giảm nhiễm trùng củ bằng cách xử lý cẩn thận trong quá trình thu hoạch để giảm thiểu vết thương cũng như tránh thu hoạch trong điều kiện ẩm ướt nếu có thể. Củ nên được bảo quản ở nhiệt độ 50 đến 55 F, ở độ ẩm tương đối cao và thông khí nhiều để thúc đẩy quá trình lành vết thương, điều này sẽ làm giảm số lượng và mức độ nghiêm trọng của nhiễm trùng củ phát triển trong quá trình bảo quản."
            })
            return HttpResponse(res, content_type='application/json', status=200)
        elif pred == 15:
            res = json.dumps({
                "tree": "Khoai tây",
                "disease": "Không có bệnh",
                "treatment": "Không có bệnh"
            })
            return HttpResponse(res, content_type='application/json', status=200)
        elif pred == 14:
            res = json.dumps({
                "tree": "Khoai tây",
                "disease": "Bệnh mốc sương (Late Blight)",
                "treatment": "Sử dụng hạt giống sạch bệnh\nTrồng đầu vụ để thoát khỏi áp lực dịch bệnh cao\nKhông để nước đọng lâu trên lá\nThường xuyên theo dõi cây và loại bỏ những cây bị nhiễm bệnh, củ bị nhiễm bệnh, cây tình nguyện và cỏ dại\nVệ sinh dụng cụ, thiết bị sau khi rời ruộng\nĐăng ký để nhận thông báo tại trang web USAblight\nGiữ củ ở nơi khô ráo và ở nhiệt độ thấp (38°F)\nGiống cây trồng chịu được khi có thể\nBảo vệ cây trồng bằng thuốc diệt nấm"
            })
            return HttpResponse(res, content_type='application/json', status=200)
        elif pred == 16:
            res = json.dumps({
                "tree": "Cà chua",
                "disease": "Bệnh đốm vi khuẩn (Bacterial Spot Disease)",
                "treatment": "Thuốc diệt nấm đồng là phương pháp điều trị được khuyên dùng phổ biến nhất đối với bệnh đốm lá do vi khuẩn. Sử dụng thuốc diệt nấm đồng như một biện pháp phòng ngừa sau khi bạn gieo hạt nhưng trước khi chuyển cây vào nơi ở cố định của chúng. Bạn có thể phun thuốc diệt nấm đồng trước hoặc sau khi mưa, nhưng không nên phun thuốc diệt nấm đồng khi trời đang mưa. Nếu bạn thấy dấu hiệu của bệnh đốm lá do vi khuẩn, hãy phun thuốc diệt nấm đồng trong thời gian từ 7 đến 10 ngày, sau đó phun lại trong một tuần sau khi cây được chuyển ra ruộng. Thực hiện xử lý bảo trì 10 ngày một lần khi thời tiết khô ráo và 5 đến 7 ngày một lần khi thời tiết mưa."
            })
            return HttpResponse(res, content_type='application/json', status=200)

        elif pred == 17:
            res = json.dumps({
                "tree": "Cà chua",
                "disease": "Bệnh bạc lá sớm (Early Blight Disease)",
                "treatment": "Cà chua bị bệnh bạc lá sớm cần được chăm sóc ngay trước khi bệnh tấn công cây. Phun kỹ cây (cả phần dưới của lá) bằng chất cô đặc thuốc diệt nấm đồng lỏng Bonide hoặc Bonide Tomato & Rau. Cả hai phương pháp xử lý này đều là hữu cơ."
            })
            return HttpResponse(res, content_type='application/json', status=200)

        elif pred == 18:
            res = json.dumps({
                "tree": "Cà chua",
                "disease": "Không có bệnh",
                "treatment": "Không có bệnh"
            })
            return HttpResponse(res, content_type='application/json', status=200)

        elif pred == 19:
            res = json.dumps({
                "tree": "Cà chua",
                "disease": "Bệnh mốc sương (Late Blight Disease)",
                "treatment": "Phun thuốc diệt nấm là cách hiệu quả nhất để ngăn ngừa bệnh mốc sương. Đối với những người làm vườn thông thường và nhà sản xuất thương mại, có thể sử dụng thuốc diệt nấm bảo vệ như chlorothalonil (ví dụ: Bravo, Echo, Equus hoặc Daconil) và Mancozeb (Manzate)."
            })
            return HttpResponse(res, content_type='application/json', status=200)

        elif pred == 20:
            res = json.dumps({
                "tree": "Cà chua",
                "disease": "Bệnh mốc lá (Leaf Mold Disease)",
                "treatment": "Sử dụng tưới nhỏ giọt và tránh tưới lá. Dùng cọc, dây hoặc tỉa cây để cây đứng vững và tăng luồng không khí trong và xung quanh cây. Loại bỏ và tiêu hủy (đốt) tất cả tàn dư thực vật sau khi thu hoạch."
            })
            return HttpResponse(res, content_type='application/json', status=200)

        elif pred == 21:
            res = json.dumps({
                "tree": "Cà chua",
                "disease": "Bệnh đốm lá Septoria (Septoria Leaf Spot Disease)",
                "treatment": "Loại bỏ những lá bị nhiễm bệnh: Loại bỏ những lá bị nhiễm bệnh ngay lập tức và nhớ rửa tay và cắt tỉa thật kỹ trước khi làm việc với những cây không bị nhiễm bệnh.\nXem xét các lựa chọn thuốc diệt nấm hữu cơ: Thuốc diệt nấm có chứa đồng hoặc kali bicarbonate sẽ giúp ngăn ngừa sự lây lan của bệnh. Bắt đầu phun thuốc ngay khi các triệu chứng đầu tiên xuất hiện và làm theo hướng dẫn trên nhãn để tiếp tục quản lý.\nXem xét thuốc diệt nấm hóa học: Mặc dù các lựa chọn hóa học không phải là lý tưởng nhưng chúng có thể là lựa chọn duy nhất để kiểm soát tình trạng nhiễm trùng nặng. Một trong những loại ít độc nhất và hiệu quả nhất là chlorothalonil (được bán dưới tên Fungonil và Daconil)."
            })
            return HttpResponse(res, content_type='application/json', status=200)

        elif pred == 22:
            res = json.dumps({
                "tree": "Cà chua",
                "disease": "Bệnh đốm mục tiêu (Target Spot Disease)",
                "treatment": "Nhiều loại thuốc diệt nấm được đăng ký để kiểm soát bệnh Target Spot trên cà chua. Người trồng nên tham khảo hướng dẫn quản lý dịch bệnh trong khu vực để biết các sản phẩm được khuyến nghị. Các sản phẩm có chứa chlorothalonil, mancozeb và copper oxychloride đã được chứng minh là có khả năng kiểm soát tốt Target Spot trong các thử nghiệm nghiên cứu"
            })
            return HttpResponse(res, content_type='application/json', status=200)
                                
        elif pred == 23:
            res = json.dumps({
                "tree": "Cà chua",
                "disease": "Bệnh virus xoăn vàng lá (Yellow Leaf Curl Virus Disease)",
                "treatment": "Kiểm tra cây để phát hiện bọ phấn trắng hai lần mỗi tuần. Nếu ruồi trắng bắt đầu xuất hiện, hãy phun azadirachtin (Neem), pyrethrin hoặc xà phòng diệt côn trùng. Để kiểm soát hiệu quả hơn, nên luân phiên ít nhất hai loại thuốc trừ sâu trên trong mỗi lần phun."
            })
            return HttpResponse(res, content_type='application/json', status=200)
                                
        elif pred == 24:
            res = json.dumps({
                "tree": "Cà chua",
                "disease": "Bệnh do virus khảm (Mosaic Virus)",
                "treatment": "Không có cách chữa trị các bệnh do virus như bệnh khảm khi cây bị nhiễm bệnh. Do đó, bạn nên nỗ lực hết sức để ngăn chặn dịch bệnh xâm nhập vào khu vườn của mình."
            })
            return HttpResponse(res, content_type='application/json', status=200)
            
        elif pred == 25:
            res = json.dumps({
                "tree": "Cà chua",
                "disease": "Bệnh nhện đỏ hai đốm (Two Spotted Spider Mite Disease)",
                "treatment": "bifenazate (Acramite): Nhóm UN, một chất độc thần kinh tồn dư lâu dài abamectin (Agri-Mek): Nhóm 6, có nguồn gốc từ vi khuẩn đất spirotetramat (Movento): Nhóm 23, chủ yếu ảnh hưởng đến giai đoạn chưa trưởng thành spiromesifen (Oberon 2SC): Nhóm 23, chủ yếu ảnh hưởng đến giai đoạn chưa trưởng thành. Các sản phẩm được liệt kê trong OMRI bao gồm: xà phòng diệt côn trùng (M-Pede)dầu neem (Bộ ba) dầu đậu nành (Dầu phun thuốc trừ sâu vàng) Với hầu hết các loại thuốc diệt bọ ve (không bao gồm bifenazate), phun 2 lần, cách nhau khoảng 5-7 ngày, để giúp kiểm soát bọ ve chưa trưởng thành đang trong giai đoạn trứng và được bảo vệ trong lần phun đầu tiên. Luân phiên giữa các sản phẩm sau 2 lần bôi giúp ngăn ngừa hoặc làm chậm tình trạng kháng thuốc."
            })
            return HttpResponse(res, content_type='application/json', status=200)
            ...