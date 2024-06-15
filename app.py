import streamlit as st
from PIL import Image
import os

st.set_page_config(page_title="Homepage", layout="wide")

def main():
    st.sidebar.title("메뉴")
    app_mode = st.sidebar.selectbox("모드 선택", ["메인 페이지", "게시판", "설문조사", "VoE", "관리자모드", "게스트모드"])
    
    if app_mode == "메인 페이지":
        show_main_page()
    elif app_mode == "게시판":
        show_board()
    elif app_mode == "설문조사":
        show_survey()
    elif app_mode == "VoE":
        show_voe()
    elif app_mode == "관리자모드":
        st.session_state["is_admin"] = True
        st.success("관리자 모드로 전환되었습니다.")
    elif app_mode == "게스트모드":
        st.session_state["is_admin"] = False
        st.success("게스트 모드로 전환되었습니다.")

def show_main_page():
    st.title("홈페이지 메인 페이지")
    st.write("여기에 홈페이지에 대한 설명을 추가하세요.")

def show_board():
    st.title("게시판")
    st.write("더블클릭 시 글을 쓸 수 있으며, 그림 파일을 업로드할 수 있습니다.")
    
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
    st.title("설문조사")
    
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
    st.title("VoE")
    
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
