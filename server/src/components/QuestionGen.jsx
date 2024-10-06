import { useRef, useState } from "react";
import { GoogleGenerativeAI } from "@google/generative-ai";
import Loading_Img from "../assets/loading.gif";
import { MdContentCopy } from "react-icons/md";
import { VscRobot } from "react-icons/vsc";

function QuestionGen() {
  const [input, setInput] = useState("");
  const [questionType, setQuestionType] = useState(""); // State for question type
  const [numQuestions, setNumQuestions] = useState(5); // State for number of questions
  const [generatedQuestions, setGeneratedQuestions] = useState([]);
  const [loading, setLoading] = useState(false);
  const copyRef = useRef();

  const genAI = new GoogleGenerativeAI(process.env.API_KEY);

  const genQuestions = async () => {
    try {
      setLoading(true);
      const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" });

      const prompt = `Generate ${numQuestions} ${questionType} questions from the following text: "${input}"`;
      
      const result = await model.generateContent(prompt);
      const response = result.response;
      const questions = response.text().split("\n").slice(0, numQuestions); // Generate the number of questions specified
      
      setInput("");
      setGeneratedQuestions(questions);
      setLoading(false);
    } catch (error) {
      console.log("Error: ", error);
      setLoading(false);
    }
  };

  const onCopyText = () => {
    copyRef.current.select();
  };

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center">
      <div className="max-w-3xl w-full md:w-2/3 lg:w-1/2 mx-4 my-8 p-6 bg-white rounded-lg shadow-lg">
        <h1 className="flex text-3xl font-bold items-center justify-center mb-4 text-white bg-gray-800 rounded-md">
          AI Question Generator
          <div className="pl-1"><VscRobot /></div>
        </h1>
        <div className="flex flex-col gap-2">
          <div className=" cursor-pointer  flex justify-end">
            <div
              className="flex bg-gray-800 text-white px-2 py-2 rounded-md hover:bg-gray-500"
              onClick={onCopyText}
            >
              Copy 
              <div className="pt-1 pl-1"><MdContentCopy size={15} /></div>
            </div>
          </div>
          <div>
            {loading === true ? (
              <div className="flex items-center justify-center border border-gray-300 rounded-md p-4 w-full h-40 resize-none focus:outline-none focus:ring-2 focus:ring-blue-500">
                <img src={Loading_Img} alt="Loading" />
              </div>
            ) : (
              <div>
                <textarea
                  className="border border-gray-300 rounded-md p-4 w-full h-40 resize-none focus:outline-none focus:ring-2 focus:ring-gray-800"
                  value={generatedQuestions.join("\n")}
                  readOnly
                  placeholder="Generated questions will appear here..."
                  ref={copyRef}
                ></textarea>
              </div>
            )}
          </div>
        </div>

        <div className="flex flex-col gap-4 pt-4">
          <textarea
            className="border border-gray-300 rounded-md py-2 px-4 w-full h-56 resize-none focus:outline-none focus:ring-2 focus:ring-gray-800"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Enter your context..."
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                return genQuestions();
              }
            }}
          />

          <div className="flex gap-4">
            <select
              className="border border-gray-300 rounded-md py-2 px-4 w-1/2 focus:outline-none focus:ring-2 focus:ring-gray-800"
              value={questionType}
              onChange={(e) => setQuestionType(e.target.value)}
            >
              <option value="" disabled>Select question type</option>
              <option value="multiple choice">Multiple Choice</option>
              <option value="true/false">True/False</option>
              <option value="short answer">Short Answer</option>
            </select>

            <input
              className="border border-gray-300 rounded-md py-2 px-4 w-1/2 focus:outline-none focus:ring-2 focus:ring-gray-800"
              value={numQuestions}
              onChange={(e) => setNumQuestions(e.target.value)}
              type="number"
              min="1"
              max="20"
              placeholder="Number of questions"
            />
          </div>

          <button
            className="ml-2 px-4 py-2 bg-gray-800 text-white rounded-md hover:bg-gray-500 focus:outline-none focus:bg-gray-500"
            onClick={genQuestions}
          >
            Generate Questions
          </button>
        </div>

        <div className="mt-8 border-gray-700 pt-8 flex flex-col items-center">
          <p className="text-sm">&copy; 2024 QnsAI Ltd. All rights reserved.</p>
        </div>
      </div>
    </div>
  );
}

export default QuestionGen;
