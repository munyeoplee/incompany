import streamlit as st
import requests
from PIL import Image
import os

st.set_page_config(page_title="Homepage", layout="wide")

def main():
    st.title("홈페이지")
    
    query_params = st.experimental_get_query_params()
    mode = query_params.get("mode", ["guest"])[0]
    
    if mode == "admin":
        st.session_state["is_admin"] = True
    else:
        st.session_state["is_admin"] = False

    # 피아노 스위치 형태의 토글 버튼
    st.markdown("""
    <style>
    .switch {
      position: relative;
      display: inline-block;
      width: 60px;
      height: 34px;
    }
    
    .switch input { 
      opacity: 0;
      width: 0;
      height: 0;
    }
    
    .slider {
      position: absolute;
      cursor: pointer;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background-color: #ccc;
      transition: .4s;
    }
    
    .slider:before {
      position: absolute;
      content: "";
      height: 26px;
      width: 26px;
      left: 4px;
      bottom: 4px;
      background-color: white;
      transition: .4s;
    }
    
    input:checked + .slider {
      background-color: #2196F3;
    }
    
    input:focus + .slider {
      box-shadow: 0 0 1px #2196F3;
    }
    
    input:checked + .slider:before {
      transform: translateX(26px);
    }
    
    /* Rounded sliders */
    .slider.round {
      border-radius: 34px;
    }
    
    .slider.round:before {
      border-radius: 50%;
    }
    </style>
    """)

    st.markdown("""
    <label class="switch">
      <input type="checkbox" id="modeSwitch" onclick="toggleMode()" {}>
      <span class="slider round"></span>
    </label>

    <script>
    function toggleMode() {{
      var checkBox = document.getElementById("modeSwitch");
      if (checkBox.checked == true){{
        window.location.href = "?mode=admin";
      }} else {{
        window.location.href = "?mode=guest";
      }}
    }}
    document.getElementById("modeSwitch").checked = {};
    </script>
    """.format("checked" if st.session_state["is_admin"] else "", "true" if st.session_state["is_admin"] else "false"), unsafe_allow_html=True)

    if st.session_state["is_admin"]:
        st.write("관리자 모드")
    else:
        st.write("게스트 모드")
    
    st.sidebar.title("메뉴")
    app_mode = st.sidebar.selectbox("모드 선택", ["메인 페이지", "게시판", "설문조사", "VoE"])
    
    if app_mode == "메인 페이지":
        show_main_page()
    elif app_mode == "게시판":
        show_board()
    elif app_mode == "설문조사":
        show_survey()
    elif app_mode == "VoE":
        show_voe()

def show_main_page():
    st.header("메인 페이지")
    st.write("여기에 홈페이지에 대한 설명을 추가하세요.")

def show_board():
    st.header("게시판")
    st.write("글을 쓰고 그림 파일을 업로드할 수 있습니다.")
    
    if "posts" not in st.session_state:
        st.session_state["posts"] = []
    
    if st.button("글쓰기"):
        with st.form("new_post"):
            title = st.text_input("제목")
            content = st.text_area("내용")
            image = st.file_uploader("이미지 업로드", type=["jpg", "png"])
            submit = st.form_submit_button("업로드")
            
            if submit:
                post = {"title": title, "content": content}
                if image:
                    image_path = os.path.join("uploads", image.name)
                    with open(image_path, "wb") as f:
                        f.write(image.getbuffer())
                    post["image"] = image_path
                st.session_state["posts"].append(post)
                st.success("게시글이 업로드되었습니다.")
    
    for post in st.session_state["posts"]:
        st.subheader(post["title"])
        st.write(post["content"])
        if "image" in post:
            st.image(post["image"])

def show_survey():
    st.header("설문조사")
    
    if "questions" not in st.session_state:
        st.session_state["questions"] = [{"question": "예시 질문", "response": ""}]
    
    if st.session_state.get("is_admin", False):
        st.write("관리자 모드에서 질문을 추가/수정할 수 있습니다.")
        if st.button("질문 추가"):
            st.session_state["questions"].append({"question": "", "response": ""})
    
    for i, q in enumerate(st.session_state["questions"]):
        if st.session_state.get("is_admin", False):
            question = st.text_input(f"질문 {i+1}", value=q["question"], key=f"question_{i}")
            st.session_state["questions"][i]["question"] = question
        else:
            st.write(f"질문 {i+1}: {q['question']}")
            response = st.text_input(f"응답 {i+1}", key=f"response_{i}")
            st.session_state["questions"][i]["response"] = response

def show_voe():
    st.header("VoE")
    
    if "voe_comments" not in st.session_state:
        st.session_state["voe_comments"] = []
    
    if not st.session_state.get("is_admin", False):
        comment = st.text_area("의견 작성")
        if st.button("작성"):
            st.session_state["voe_comments"].append({"comment": comment, "admin_response": ""})
            st.success("의견이 작성되었습니다.")
    
    for i, voe in enumerate(st.session_state["voe_comments"]):
        st.write(f"{i+1}. {voe['comment']}")
        if st.session_state.get("is_admin", False):
            response = st.text_input(f"관리자 응답 {i+1}", key=f"admin_response_{i}")
            st.session_state["voe_comments"][i]["admin_response"] = response
            st.write(f"관리자 응답: {voe['admin_response']}")
        else:
            if voe["admin_response"]:
                st.write(f"관리자 응답: {voe['admin_response']}")

if __name__ == "__main__":
    if "is_admin" not in st.session_state:
        st.session_state["is_admin"] = False
    main()
