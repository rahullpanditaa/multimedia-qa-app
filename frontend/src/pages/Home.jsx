import FileUpload from "../components/FileUpload";
import ChatBox from "../components/ChatBox";

// Home Page
function Home() {
  return (
    <div>
      <h1>Multimedia RAG Application</h1>

      <FileUpload />

      <hr />

      <ChatBox />
    </div>
  );
}

export default Home;