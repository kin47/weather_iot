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
        # if image:
        #     image_bytes = image.read()

            # Convert the image bytes to a numpy array
            # nparr = np.frombuffer(image_bytes, np.uint8)
            # image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            # cv2.imshow('image', image)

            # image = cv2.resize(image, (128, 128))
            # image = (
            #     img_to_array(image) / 255
            # )  # convert image to np array and normalize
            # image = np.expand_dims(image, axis=0)  # change dimention 3D to 4D

            # # Make predictions
            # result = model.predict(image)

            # pred = np.argmax(result, axis=1)[0]
            # print('@@ RAW Result', pred)
        if pred == 0:
            res = json.dumps({
                "tree": "Cà chua",
                "disease": "Bệnh đốm vi khuẩn (Bacterial Spot Disease)",
                "treatment": "Thuốc diệt nấm đồng là phương pháp điều trị được khuyên dùng phổ biến nhất đối với bệnh đốm lá do vi khuẩn. Sử dụng thuốc diệt nấm đồng như một biện pháp phòng ngừa sau khi bạn gieo hạt nhưng trước khi chuyển cây vào nơi ở cố định của chúng. Bạn có thể phun thuốc diệt nấm đồng trước hoặc sau khi mưa, nhưng không nên phun thuốc diệt nấm đồng khi trời đang mưa. Nếu bạn thấy dấu hiệu của bệnh đốm lá do vi khuẩn, hãy phun thuốc diệt nấm đồng trong thời gian từ 7 đến 10 ngày, sau đó phun lại trong một tuần sau khi cây được chuyển ra ruộng. Thực hiện xử lý bảo trì 10 ngày một lần khi thời tiết khô ráo và 5 đến 7 ngày một lần khi thời tiết mưa."
            })
            return HttpResponse(res, content_type='application/json', status=200)

        elif pred == 1:
            res = json.dumps({
                "tree": "Cà chua",
                "disease": "Bệnh bạc lá sớm (Early Blight Disease)",
                "treatment": "Cà chua bị bệnh bạc lá sớm cần được chăm sóc ngay trước khi bệnh tấn công cây. Phun kỹ cây (cả phần dưới của lá) bằng chất cô đặc thuốc diệt nấm đồng lỏng Bonide hoặc Bonide Tomato & Rau. Cả hai phương pháp xử lý này đều là hữu cơ."
            })
            return HttpResponse(res, content_type='application/json', status=200)

        elif pred == 2:
            res = json.dumps({
                "tree": "Cà chua",
                "disease": "Không có bệnh",
                "treatment": "Không có bệnh"
            })
            return HttpResponse(res, content_type='application/json', status=200)

        elif pred == 3:
            res = json.dumps({
                "tree": "Cà chua",
                "disease": "Bệnh mốc sương (Late Blight Disease)",
                "treatment": "Phun thuốc diệt nấm là cách hiệu quả nhất để ngăn ngừa bệnh mốc sương. Đối với những người làm vườn thông thường và nhà sản xuất thương mại, có thể sử dụng thuốc diệt nấm bảo vệ như chlorothalonil (ví dụ: Bravo, Echo, Equus hoặc Daconil) và Mancozeb (Manzate)."
            })
            return HttpResponse(res, content_type='application/json', status=200)

        elif pred == 4:
            res = json.dumps({
                "tree": "Cà chua",
                "disease": "Bệnh mốc lá (Leaf Mold Disease)",
                "treatment": "Sử dụng tưới nhỏ giọt và tránh tưới lá. Dùng cọc, dây hoặc tỉa cây để cây đứng vững và tăng luồng không khí trong và xung quanh cây. Loại bỏ và tiêu hủy (đốt) tất cả tàn dư thực vật sau khi thu hoạch."
            })
            return HttpResponse(res, content_type='application/json', status=200)

        elif pred == 5:
            res = json.dumps({
                "tree": "Cà chua",
                "disease": "Bệnh đốm lá Septoria (Septoria Leaf Spot Disease)",
                "treatment": "Loại bỏ những lá bị nhiễm bệnh: Loại bỏ những lá bị nhiễm bệnh ngay lập tức và nhớ rửa tay và cắt tỉa thật kỹ trước khi làm việc với những cây không bị nhiễm bệnh.\nXem xét các lựa chọn thuốc diệt nấm hữu cơ: Thuốc diệt nấm có chứa đồng hoặc kali bicarbonate sẽ giúp ngăn ngừa sự lây lan của bệnh. Bắt đầu phun thuốc ngay khi các triệu chứng đầu tiên xuất hiện và làm theo hướng dẫn trên nhãn để tiếp tục quản lý.\nXem xét thuốc diệt nấm hóa học: Mặc dù các lựa chọn hóa học không phải là lý tưởng nhưng chúng có thể là lựa chọn duy nhất để kiểm soát tình trạng nhiễm trùng nặng. Một trong những loại ít độc nhất và hiệu quả nhất là chlorothalonil (được bán dưới tên Fungonil và Daconil)."
            })
            return HttpResponse(res, content_type='application/json', status=200)

        elif pred == 6:
            res = json.dumps({
                "tree": "Cà chua",
                "disease": "Bệnh đốm mục tiêu (Target Spot Disease)",
                "treatment": "Nhiều loại thuốc diệt nấm được đăng ký để kiểm soát bệnh Target Spot trên cà chua. Người trồng nên tham khảo hướng dẫn quản lý dịch bệnh trong khu vực để biết các sản phẩm được khuyến nghị. Các sản phẩm có chứa chlorothalonil, mancozeb và copper oxychloride đã được chứng minh là có khả năng kiểm soát tốt Target Spot trong các thử nghiệm nghiên cứu"
            })
            return HttpResponse(res, content_type='application/json', status=200)
                                
        elif pred == 7:
            res = json.dumps({
                "tree": "Cà chua",
                "disease": "Bệnh virus xoăn vàng lá (Yellow Leaf Curl Virus Disease)",
                "treatment": "Kiểm tra cây để phát hiện bọ phấn trắng hai lần mỗi tuần. Nếu ruồi trắng bắt đầu xuất hiện, hãy phun azadirachtin (Neem), pyrethrin hoặc xà phòng diệt côn trùng. Để kiểm soát hiệu quả hơn, nên luân phiên ít nhất hai loại thuốc trừ sâu trên trong mỗi lần phun."
            })
            return HttpResponse(res, content_type='application/json', status=200)
                                
        elif pred == 8:
            res = json.dumps({
                "tree": "Cà chua",
                "disease": "Bệnh do virus khảm (Mosaic Virus)",
                "treatment": "Không có cách chữa trị các bệnh do virus như bệnh khảm khi cây bị nhiễm bệnh. Do đó, bạn nên nỗ lực hết sức để ngăn chặn dịch bệnh xâm nhập vào khu vườn của mình."
            })
            return HttpResponse(res, content_type='application/json', status=200)
            
        elif pred == 9:
            res = json.dumps({
                "tree": "Cà chua",
                "disease": "Bệnh nhện đỏ hai đốm (Two Spotted Spider Mite Disease)",
                "treatment": "bifenazate (Acramite): Nhóm UN, một chất độc thần kinh tồn dư lâu dài abamectin (Agri-Mek): Nhóm 6, có nguồn gốc từ vi khuẩn đất spirotetramat (Movento): Nhóm 23, chủ yếu ảnh hưởng đến giai đoạn chưa trưởng thành spiromesifen (Oberon 2SC): Nhóm 23, chủ yếu ảnh hưởng đến giai đoạn chưa trưởng thành. Các sản phẩm được liệt kê trong OMRI bao gồm: xà phòng diệt côn trùng (M-Pede)dầu neem (Bộ ba) dầu đậu nành (Dầu phun thuốc trừ sâu vàng) Với hầu hết các loại thuốc diệt bọ ve (không bao gồm bifenazate), phun 2 lần, cách nhau khoảng 5-7 ngày, để giúp kiểm soát bọ ve chưa trưởng thành đang trong giai đoạn trứng và được bảo vệ trong lần phun đầu tiên. Luân phiên giữa các sản phẩm sau 2 lần bôi giúp ngăn ngừa hoặc làm chậm tình trạng kháng thuốc."
            })
            return HttpResponse(res, content_type='application/json', status=200)
            ...