import FileUpload from "../components/FileUpload";
import ChatBox from "../components/ChatBox";

function Home() {
  return (
    <div>
      <h1>Multimedia RAG Application</h1>

      <FileUpload />

      <ChatBox />
    </div>
  );
}

export default Home;