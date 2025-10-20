import Model_card from '../components/model_card'
import  naive_logo  from "../assets/images/naive-bays.png";
import n_gram from "../assets/images/n-gram-logo.png";
import log_reg from "../assets/images/log-reg.png";

function Home_page(){
    return (
    <>
      <div className="text-5xl flex flex-row mt-25 justify-center items-center mb-25">
        Choose NLP Model
      </div>
      <div className='flex flex-col md:flex-row justify-between items-center md:items-stretch mx-5 md:mx-20 gap-5 mt-5'>
        <Model_card destination={"/n-gram"} icon={n_gram} model_name={"N-gram"} model_description={"A model to predict the next word in a sentence."}></Model_card>
        <Model_card destination={"/naive-bays"} icon={naive_logo} model_name={"Naive bays"} model_description={"A model for Spam messages detection using Naive Bays algorithm."}></Model_card>
        <Model_card destination={"/log-reg"} icon={log_reg} model_name={"Logistic Regression"} model_description={"A model for spam message detection using Logistic regression algorithm."} ></Model_card>
      </div>
    </>);
}

export default Home_page;