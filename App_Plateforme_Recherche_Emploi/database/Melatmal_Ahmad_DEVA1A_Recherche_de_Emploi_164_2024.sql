-- OM 2021.02.17
-- FICHIER MYSQL POUR FAIRE FONCTIONNER LES EXEMPLES
-- DE REQUETES MYSQL
-- Database: Melatmal_Ahmad_DEVA1A_Recherche_de_Emploi_164_2024.sql

-- Destruction de la BD si elle existe.
-- Pour être certain d'avoir la dernière version des données

DROP DATABASE IF EXISTS Melatmal_Ahmad_DEVA1A_Recherche_de_Emploi_164_2024;

-- Création d'un nouvelle base de donnée

CREATE DATABASE IF NOT EXISTS Melatmal_Ahmad_DEVA1A_Recherche_de_Emploi_164_2024;

-- Utilisation de cette base de donnée

USE Melatmal_Ahmad_DEVA1A_Recherche_de_Emploi_164_2024;
-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1
-- Généré le : mer. 22 mai 2024 à 19:12
-- Version du serveur : 10.4.32-MariaDB
-- Version de PHP : 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `melatmal_ahmad_dev1a_mpd`
--

-- --------------------------------------------------------

--
-- Table structure for table `t_candidat`
--

CREATE TABLE `t_candidat` (
  `ID_Candidat` int(11) NOT NULL,
  `Nom` varchar(100) NOT NULL,
  `Prenom` varchar(100) NOT NULL,
  `Email` varchar(255) NOT NULL,
  `Mot_de_passe` varchar(255) NOT NULL,
  `Telephone` varchar(20) DEFAULT NULL,
  `Date_de_naissance` date DEFAULT NULL,
  `Adresse` varchar(255) DEFAULT NULL,
  `Titre_profil` varchar(255) DEFAULT NULL,
  `Resume` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `t_candidat`
--

INSERT INTO `t_candidat` (`ID_Candidat`, `Nom`, `Prenom`, `Email`, `Mot_de_passe`, `Telephone`, `Date_de_naissance`, `Adresse`, `Titre_profil`, `Resume`) VALUES
(1, 'Smith', 'John', 'smith@example.com', 'password1', '+1234567890', '1990-05-15', '123 Main Street, Cityville', 'Software Engineer', 'Experienced software engineer with expertise in Java and Python.'),
(2, 'Johnson', 'Emily', 'emily.j@example.com', 'pass123', '+1987654321', '1985-12-28', '456 Oak Avenue, Townsville', 'Data Scientist', 'Data scientist skilled in machine learning and data analysis.'),
(3, 'Garcia', 'Luis', 'lgarcia@example.com', 'securepass', '+1555098765', '1992-08-03', '789 Elm Drive, Villageton', 'Web Developer', 'Frontend web developer proficient in HTML, CSS, and JavaScript.'),
(4, 'Kim', 'Soojin', 'skim@example.com', 'mysecret', '+17778889999', '1988-02-10', '987 Pine Road, Hamletown', 'UX/UI Designer', 'Creative UX/UI designer passionate about user-centered design.'),
(5, 'Chen', 'Wei', 'wchen@example.com', 'weipass', '+16667778888', '1995-07-20', '654 Maple Lane, Suburbia', 'Marketing Specialist', 'Marketing specialist with experience in digital marketing and social media management.'),
(6, 'Patel', 'Raj', 'rpatel@example.com', 'raj1234', '+18889997777', '1993-11-07', '321 Cedar Street, Countryside', 'Business Analyst', 'Analytical business analyst with expertise in data-driven decision making.'),
(7, 'Martinez', 'Maria', 'mmartinez@example.com', 'maria321', '+14445556666', '1991-04-12', '852 Birch Avenue, Cityside', 'Graphic Designer', 'Talented graphic designer skilled in Adobe Creative Suite.'),
(8, 'Brown', 'Emma', 'ebrown@example.com', 'emma456', '+13334447777', '1987-09-25', '159 Walnut Drive, Metropolis', 'Project Manager', 'Certified project manager with experience in agile methodologies.'),
(9, 'Nguyen', 'Minh', 'mnguyen@example.com', 'minhpass', '+12223334444', '1994-03-30', '753 Oak Street, Townsville', 'Software Developer', 'Full-stack developer proficient in React, Node.js, and SQL.'),
(10, 'Suzuki', 'Yuki', 'ysuzuki@example.com', 'yukipass', '+19998887777', '1990-06-18', '357 Elm Avenue, Villageton', 'Network Engineer', 'Network engineer specializing in Cisco systems and network security.'),
(11, 'Wong', 'Li', 'lwong@example.com', 'li987', '+18887776666', '1989-10-09', '852 Pine Lane, Suburbia', 'Digital Marketer', 'Experienced digital marketer with a focus on SEO and SEM strategies.'),
(12, 'Gomez', 'Javier', 'javier@example.com', 'jav123', '+17776665555', '1996-01-24', '963 Maple Drive, Hamletown', 'UI Designer', 'UI designer passionate about creating intuitive user interfaces.'),
(13, 'Taylor', 'Olivia', 'olivia.t@example.com', 'taylorpass', '+16665554444', '1986-11-15', '741 Cedar Street, Countryside', 'Data Analyst', 'Detail-oriented data analyst with expertise in statistical analysis.'),
(14, 'Lee', 'Sung', 'slee@example.com', 'sung321', '+14443332222', '1992-05-08', '852 Birch Avenue, Cityside', 'Product Manager', 'Innovative product manager experienced in product development lifecycle.'),
(15, 'Jackson', 'Michael', 'mjackson@example.com', 'mikepass', '+13332221111', '1984-08-29', '159 Walnut Drive, Metropolis', 'System Administrator', 'System administrator proficient in Linux and Windows server administration.');

-- --------------------------------------------------------

--
-- Table structure for table `t_candidature`
--

CREATE TABLE `t_candidature` (
  `ID_Candidature` int(11) NOT NULL,
  `FK_Candidat` int(11) NOT NULL,
  `FK_Offre` int(11) NOT NULL,
  `Date_Candidature` date NOT NULL,
  `Lettre_Motivation` text DEFAULT NULL,
  `Statut` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `t_candidature`
--

INSERT INTO `t_candidature` (`ID_Candidature`, `FK_Candidat`, `FK_Offre`, `Date_Candidature`, `Lettre_Motivation`, `Statut`) VALUES
(1, 3, 7, '2024-03-10', 'Dear Hiring Manager,\nI am writing to express my interest in the Supply Chain Manager position at Logistics Solutions Inc. I have extensive experience in logistics and inventory management, and I am confident in my ability to drive efficiency and optimize processes in your organization.\n\nSincerely, [Candidate]', 'Pending'),
(2, 8, 3, '2024-03-11', 'Dear Hiring Manager,\nI am excited to apply for the Software Developer position at HealthTech Solutions. With my background in healthcare IT and proficiency in programming languages, I am eager to contribute to the development of innovative healthcare software solutions.\n\nBest regards, [Candidate]', 'Pending'),
(3, 1, 10, '2024-03-12', 'Dear Hiring Manager,\nI am writing to apply for the Research Analyst position at Healthcare Innovations Group. With my strong analytical skills and background in healthcare research, I am confident in my ability to conduct impactful research and contribute to your team.\n\nSincerely, [Candidate]', 'Pending'),
(4, 6, 2, '2024-03-13', 'Dear Hiring Manager,\nI am thrilled to apply for the Financial Analyst position at Global Finance Group. With my expertise in financial analysis and strategic management, I am eager to support your finance team and drive business success.\n\nBest regards, [Candidate]', 'Pending'),
(5, 12, 9, '2024-03-14', 'Dear Hiring Manager,\nI am writing to express my interest in the Project Manager position at Construction Dynamics. With my strong project management skills and experience in construction, I am confident in my ability to oversee successful construction projects.\n\nSincerely, [Candidate]', 'Pending'),
(6, 9, 4, '2024-03-15', 'Dear Hiring Manager,\nI am excited to apply for the Digital Marketing Manager position at Marketing Pro Agency. With my expertise in digital marketing strategies, I am eager to drive results and contribute to your team\'s success.\n\nBest regards, [Candidate]', 'Pending'),
(7, 5, 12, '2024-03-16', 'Dear Hiring Manager,\nI am writing to express my interest in the Management Consultant position at Consulting Solutions LLC. With my strong problem-solving skills and experience in business consulting, I am confident in my ability to provide valuable insights and recommendations to your clients.\n\nSincerely, [Candidate]', 'Pending'),
(8, 11, 6, '2024-03-17', 'Dear Hiring Manager,\nI am thrilled to apply for the Graphic Designer position at Creative Design Studio. With my creative skills and expertise in graphic design software, I am eager to bring visual concepts to life and deliver impactful designs for your clients.\n\nBest regards, [Candidate]', 'Pending'),
(9, 10, 15, '2024-03-18', 'Dear Hiring Manager,\nI am writing to apply for the Systems Administrator position at Tech Innovations Inc. With my strong technical skills and experience in system administration, I am confident in my ability to maintain and optimize IT systems for your organization.\n\nSincerely, [Candidate]', 'Pending'),
(10, 2, 8, '2024-03-19', 'Dear Hiring Manager,\nI am excited to apply for the Venture Capital Analyst position at TechStart Ventures. With my strong financial analysis skills and passion for technology, I am eager to evaluate investment opportunities and support the growth of technology startups.\n\nBest regards, [Candidate]', 'Pending'),
(11, 14, 14, '2024-03-20', 'Dear Hiring Manager,\nI am thrilled to apply for the Product Manager position at Global Healthcare Solutions. With my strong product management skills and background in healthcare IT, I am eager to lead the development and launch of innovative healthcare software products.\n\nSincerely, [Candidate]', 'Pending'),
(12, 4, 1, '2024-03-21', 'Dear Hiring Manager,\nI am writing to express my interest in the Senior Software Engineer position at Tech Innovations Inc. With my expertise in software development and passion for innovation, I am eager to contribute to your team and drive the development of cutting-edge software solutions.\n\nBest regards, [Candidate]', 'Pending'),
(13, 7, 11, '2024-03-22', 'Dear Hiring Manager,\nI am excited to apply for the Research Scientist position at InnovateX Inc. With my background in research and development, I am eager to contribute to cutting-edge projects and drive scientific innovation.\n\nBest regards, [Candidate]', 'Pending'),
(14, 13, 13, '2024-03-23', 'Dear Hiring Manager,\nI am writing to express my interest in the Systems Engineer position at TechCorp Industries. With my strong technical skills and experience in system administration, I am confident in my ability to design and implement IT solutions to meet your organization\'s needs.\n\nSincerely, [Candidate]', 'Pending'),
(15, 15, 5, '2024-03-24', 'Dear Hiring Manager,\nI am thrilled to apply for the Environmental Consultant position at EcoFriendly Solutions. With my knowledge of environmental science and experience in environmental consulting, I am eager to contribute to sustainable solutions and environmental protection.\n\nBest regards, [Candidate]', 'Pending');

-- --------------------------------------------------------

--
-- Table structure for table `t_competence`
--

CREATE TABLE `t_competence` (
  `ID_Competence` int(11) NOT NULL,
  `Nom_Competence` varchar(100) NOT NULL,
  `Description` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `t_competence`
--

INSERT INTO `t_competence` (`ID_Competence`, `Nom_Competence`, `Description`) VALUES
(1, 'Project Management', 'Ability to plan, execute, and oversee projects from inception to completion, including managing resources, timelines, and budgets.'),
(2, 'Data Analysis', 'Proficiency in analyzing and interpreting data to extract meaningful insights and inform decision-making processes.'),
(3, 'Web Development', 'Skill in designing and developing websites and web applications using various programming languages and frameworks such as HTML, CSS, JavaScript, and React.'),
(4, 'Graphic Design', 'Expertise in creating visual content for digital and print media, including logos, brochures, posters, and advertisements, using graphic design software like Adobe Photoshop and Illustrator.'),
(5, 'Leadership', 'Ability to inspire and motivate others to achieve common goals, while providing direction, support, and guidance.'),
(6, 'Digital Marketing', 'Knowledge of online marketing strategies and techniques to promote products or services through digital channels such as social media, email, and search engines.'),
(7, 'Database Management', 'Skill in designing, implementing, and maintaining databases to ensure data integrity, security, and performance.'),
(8, 'Problem Solving', 'Ability to identify and analyze complex problems, develop innovative solutions, and implement effective strategies to address challenges.'),
(9, 'Communication Skills', 'Proficiency in conveying information clearly and effectively through verbal, written, and visual means, while actively listening and responding appropriately.'),
(10, 'Software Development', 'Experience in designing, coding, testing, and debugging software applications to meet specific requirements and deliver high-quality solutions.'),
(11, 'Network Security', 'Knowledge of security protocols, encryption techniques, and intrusion detection systems to protect computer networks and data from unauthorized access and cyber threats.'),
(12, 'Financial Analysis', 'Skill in evaluating financial data, trends, and performance metrics to assess the financial health and viability of an organization, and make informed recommendations for improvement.'),
(13, 'UI/UX Design', 'Expertise in creating intuitive user interfaces and engaging user experiences for websites, mobile apps, and software products, while considering usability and accessibility.'),
(14, 'Content Writing', 'Ability to create compelling and informative content for various platforms and audiences, including blogs, articles, website copy, and social media posts.'),
(15, 'Time Management', 'Skill in prioritizing tasks, managing schedules, and allocating time effectively to maximize productivity and achieve goals in a timely manner.');

-- --------------------------------------------------------

--
-- Table structure for table `t_competences_candidat`
--

CREATE TABLE `t_competences_candidat` (
  `FK_Candidat` int(11) NOT NULL,
  `FK_Competence` int(11) NOT NULL,
  `Niveau` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `t_competences_candidat`
--

INSERT INTO `t_competences_candidat` (`FK_Candidat`, `FK_Competence`, `Niveau`) VALUES
(1, 3, 'Intermediate'),
(2, 7, 'Advanced'),
(3, 11, 'Expert'),
(4, 5, 'Intermediate'),
(5, 9, 'Advanced'),
(6, 2, 'Expert'),
(7, 10, 'Intermediate'),
(8, 12, 'Advanced'),
(9, 6, 'Intermediate'),
(10, 14, 'Expert'),
(11, 1, 'Advanced'),
(12, 8, 'Intermediate'),
(13, 4, 'Advanced'),
(14, 13, 'Intermediate'),
(15, 15, 'Advanced');

-- --------------------------------------------------------

--
-- Table structure for table `t_employeur`
--

CREATE TABLE `t_employeur` (
  `ID_Employeur` int(11) NOT NULL,
  `Nom_Entreprise` varchar(255) NOT NULL,
  `Secteur` varchar(100) DEFAULT NULL,
  `Email` varchar(255) NOT NULL,
  `Telephone` varchar(20) DEFAULT NULL,
  `Adresse` varchar(255) DEFAULT NULL,
  `Description` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `t_employeur`
--

INSERT INTO `t_employeur` (`ID_Employeur`, `Nom_Entreprise`, `Secteur`, `Email`, `Telephone`, `Adresse`, `Description`) VALUES
(1, 'Tech Innovations Inc.', 'Technology', 'info@techinnovations.com', '+1234567890', '123 Main Street, Cityville', 'Tech Innovations Inc. is a leading technology company specializing in software development and IT solutions.'),
(2, 'Global Finance Group', 'Finance', 'contact@globalfinancegroup.com', '+1987654321', '456 Oak Avenue, Townsville', 'Global Finance Group is a multinational financial services corporation offering banking, investment, and insurance services worldwide.'),
(3, 'HealthTech Solutions', 'Healthcare', 'info@healthtechsolutions.com', '+1555098765', '789 Elm Drive, Villageton', 'HealthTech Solutions is dedicated to improving healthcare through innovative technology solutions, including electronic medical records and telemedicine platforms.'),
(4, 'Green Energy Corp', 'Renewable Energy', 'info@greenenergycorp.com', '+17778889999', '987 Pine Road, Hamletown', 'Green Energy Corp is committed to promoting sustainability and reducing carbon emissions through the development and implementation of renewable energy solutions.'),
(5, 'Marketing Pro Agency', 'Marketing', 'contact@marketingproagency.com', '+16667778888', '654 Maple Lane, Suburbia', 'Marketing Pro Agency offers comprehensive digital marketing services, including SEO, SEM, social media management, and content marketing strategies.'),
(6, 'Consulting Solutions LLC', 'Consulting', 'info@consultingsolutions.com', '+18889997777', '321 Cedar Street, Countryside', 'Consulting Solutions LLC provides strategic consulting services to businesses across various industries, specializing in business development, operations, and management.'),
(7, 'Creative Design Studio', 'Design', 'info@creativedesignstudio.com', '+14445556666', '852 Birch Avenue, Cityside', 'Creative Design Studio is a boutique design agency offering creative solutions for branding, graphic design, and web development projects.'),
(8, 'Logistics Solutions Inc.', 'Logistics', 'contact@logisticssolutions.com', '+13334447777', '159 Walnut Drive, Metropolis', 'Logistics Solutions Inc. provides end-to-end logistics and supply chain management services, optimizing efficiency and reducing costs for businesses worldwide.'),
(9, 'TechStart Ventures', 'Venture Capital', 'info@techstartventures.com', '+12223334444', '753 Oak Street, Townsville', 'TechStart Ventures is a venture capital firm specializing in early-stage investments in technology startups, supporting innovation and entrepreneurship.'),
(10, 'Construction Dynamics', 'Construction', 'info@constructiondynamics.com', '+19998887777', '357 Elm Avenue, Villageton', 'Construction Dynamics is a full-service construction company offering design-build, general contracting, and project management services for residential and commercial projects.'),
(11, 'Healthcare Innovations Group', 'Healthcare', 'info@healthcareinnovationsgroup.com', '+18887776666', '852 Pine Lane, Suburbia', 'Healthcare Innovations Group is dedicated to driving innovation and improving patient outcomes in healthcare through research, development, and collaboration with industry partners.'),
(12, 'EcoFriendly Solutions', 'Environmental Services', 'info@ecofriendlysolutions.com', '+17776665555', '963 Maple Drive, Hamletown', 'EcoFriendly Solutions provides eco-friendly products and services to businesses and consumers, promoting sustainability and environmental responsibility.'),
(13, 'TechCorp Industries', 'Technology', 'info@techcorpindustries.com', '+16665554444', '741 Cedar Street, Countryside', 'TechCorp Industries is a leading technology company specializing in hardware and software solutions for businesses, government agencies, and educational institutions.'),
(14, 'InnovateX Inc.', 'Technology', 'info@innovatexinc.com', '+14443332222', '852 Birch Avenue, Cityside', 'InnovateX Inc. is dedicated to driving innovation and technological advancement through research, development, and commercialization of cutting-edge technologies.'),
(15, 'Global Healthcare Solutions', 'Healthcare', 'info@globalhealthcaresolutions.com', '+13332221111', '159 Walnut Drive, Metropolis', 'Global Healthcare Solutions is committed to improving healthcare access and quality worldwide through innovative solutions and partnerships with healthcare providers and organizations.');

-- --------------------------------------------------------

--
-- Table structure for table `t_experience_professionnelle`
--

CREATE TABLE `t_experience_professionnelle` (
  `ID_Experience` int(11) NOT NULL,
  `FK_Candidat` int(11) NOT NULL,
  `Entreprise` varchar(255) NOT NULL,
  `Titre_Poste` varchar(100) NOT NULL,
  `Date_Debut` date NOT NULL,
  `Date_Fin` date DEFAULT NULL,
  `Description` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `t_experience_professionnelle`
--

INSERT INTO `t_experience_professionnelle` (`ID_Experience`, `FK_Candidat`, `Entreprise`, `Titre_Poste`, `Date_Debut`, `Date_Fin`, `Description`) VALUES
(1, 3, 'Tech Innovations Inc.', 'Senior Software Engineer', '2018-06-15', '2022-09-30', 'Led a team of developers in the design and implementation of innovative software solutions for clients. Collaborated with cross-functional teams to deliver high-quality products on time and within budget.'),
(2, 8, 'Global Finance Group', 'Financial Analyst', '2019-03-01', '2021-12-31', 'Conducted financial analysis and modeling to evaluate investment opportunities and assess risk. Prepared reports and presentations for senior management to support decision-making processes.'),
(3, 1, 'HealthTech Solutions', 'Software Developer', '2020-01-15', '2023-05-20', 'Developed and maintained healthcare software applications, including electronic medical records systems and telemedicine platforms. Collaborated with healthcare professionals to understand user requirements and implement software enhancements.'),
(4, 6, 'Marketing Pro Agency', 'Digital Marketing Manager', '2017-09-10', '2022-03-15', 'Developed and executed digital marketing campaigns across multiple channels, including social media, email, and search engines. Analyzed campaign performance metrics and adjusted strategies to optimize results.'),
(5, 12, 'Consulting Solutions LLC', 'Management Consultant', '2018-11-20', '2021-08-30', 'Provided strategic consulting services to clients in various industries, including market research, business development, and operational improvement. Developed actionable recommendations and implementation plans to drive client success.'),
(6, 9, 'Creative Design Studio', 'Graphic Designer', '2019-07-05', '2023-10-10', 'Created visually compelling designs for clients across diverse industries, including branding, print materials, and digital assets. Collaborated with clients to understand their vision and translate it into effective design solutions.'),
(7, 5, 'Logistics Solutions Inc.', 'Supply Chain Manager', '2018-04-15', '2022-06-30', 'Managed end-to-end supply chain operations, including procurement, inventory management, and distribution. Implemented process improvements to optimize efficiency and reduce costs throughout the supply chain.'),
(8, 11, 'TechStart Ventures', 'Venture Capital Analyst', '2020-02-01', '2023-04-30', 'Evaluated investment opportunities in technology startups, conducted due diligence, and prepared investment recommendations for the firm\'s partners. Monitored portfolio companies and provided support as needed to drive growth and success.'),
(9, 10, 'Construction Dynamics', 'Project Manager', '2017-08-20', '2021-11-15', 'Managed residential and commercial construction projects from planning through completion, including budgeting, scheduling, and subcontractor coordination. Ensured projects were delivered on time and met quality standards.'),
(10, 2, 'Healthcare Innovations Group', 'Research Analyst', '2019-01-10', '2022-07-25', 'Conducted research on healthcare trends, technologies, and best practices to support the development of innovative healthcare solutions. Analyzed market data and competitor information to identify opportunities for growth and differentiation.'),
(11, 14, 'EcoFriendly Solutions', 'Environmental Consultant', '2018-05-05', '2023-09-10', 'Provided environmental consulting services to businesses and organizations, including environmental impact assessments, regulatory compliance, and sustainability planning. Developed strategies to minimize environmental risks and promote eco-friendly practices.'),
(12, 4, 'TechCorp Industries', 'Systems Engineer', '2017-10-15', '2021-12-20', 'Designed and implemented complex IT systems and infrastructure solutions for clients, including network architecture, server deployment, and security configurations. Provided technical expertise and support throughout the project lifecycle.'),
(13, 7, 'InnovateX Inc.', 'Research Scientist', '2019-02-28', '2023-08-15', 'Conducted research and development of advanced technologies in collaboration with interdisciplinary teams. Published findings in peer-reviewed journals and presented research at industry conferences and events.'),
(14, 13, 'Global Healthcare Solutions', 'Product Manager', '2018-09-10', '2022-11-30', 'Managed the development and launch of healthcare software products, including product definition, feature prioritization, and go-to-market strategy. Worked closely with engineering, marketing, and sales teams to drive product success.'),
(15, 15, 'Tech Innovations Inc.', 'Systems Administrator', '2017-06-20', '2021-10-05', 'Administered and maintained IT systems and infrastructure, including servers, networks, and databases. Implemented security measures to protect against cyber threats and ensure data integrity and confidentiality.');

-- --------------------------------------------------------

--
-- Table structure for table `t_formation`
--

CREATE TABLE `t_formation` (
  `ID_Formation` int(11) NOT NULL,
  `FK_Candidat` int(11) NOT NULL,
  `Etablissement` varchar(255) NOT NULL,
  `Diplome` varchar(100) NOT NULL,
  `Domaine` varchar(100) NOT NULL,
  `Date_Debut` date NOT NULL,
  `Date_Fin` date DEFAULT NULL,
  `Description` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `t_formation`
--

INSERT INTO `t_formation` (`ID_Formation`, `FK_Candidat`, `Etablissement`, `Diplome`, `Domaine`, `Date_Debut`, `Date_Fin`, `Description`) VALUES
(1, 3, 'University of Science and Technology', 'Bachelor of Science in Computer Science', 'Computer Science', '2016-09-01', '2020-06-30', 'Completed coursework in algorithms, data structures, programming languages, and software engineering principles.'),
(2, 8, 'Finance Academy', 'Master of Business Administration (MBA)', 'Business Administration', '2017-08-15', '2019-05-30', 'Specialized in finance and strategic management, with coursework in financial analysis, investment strategies, and corporate finance.'),
(3, 1, 'Healthcare Institute', 'Master of Science in Health Informatics', 'Health Informatics', '2018-01-10', '2020-12-20', 'Studied healthcare information systems, electronic health records, health data analytics, and regulatory compliance.'),
(4, 6, 'Digital Marketing Institute', 'Professional Diploma in Digital Marketing', 'Digital Marketing', '2016-07-01', '2017-12-15', 'Acquired skills in SEO, social media marketing, email marketing, content strategy, and digital analytics.'),
(5, 12, 'Business Consulting School', 'Certificate in Management Consulting', 'Management Consulting', '2017-10-05', '2018-11-30', 'Focused on strategic planning, organizational development, project management, and client engagement strategies.'),
(6, 9, 'Design Academy', 'Bachelor of Fine Arts in Graphic Design', 'Graphic Design', '2016-09-01', '2020-05-30', 'Developed proficiency in visual communication, typography, branding, and multimedia design through hands-on projects and coursework.'),
(7, 5, 'Supply Chain University', 'Certificate in Supply Chain Management', 'Supply Chain Management', '2017-02-15', '2018-11-20', 'Explored topics such as logistics, inventory management, procurement, and supply chain optimization strategies.'),
(8, 11, 'Venture Capital Institute', 'Certificate in Venture Capital and Private Equity', 'Venture Capital', '2018-03-01', '2019-06-30', 'Learned about venture capital financing, investment analysis, due diligence, and portfolio management strategies.'),
(9, 10, 'Construction Management School', 'Bachelor of Science in Construction Management', 'Construction Management', '2015-09-01', '2019-05-30', 'Studied construction project management, building codes, construction technology, and safety regulations.'),
(10, 2, 'Healthcare Research Institute', 'Certificate in Healthcare Research Methods', 'Healthcare Research', '2016-08-15', '2017-12-20', 'Focused on research design, data collection methods, statistical analysis, and ethical considerations in healthcare research.'),
(11, 14, 'Environmental Science Academy', 'Master of Science in Environmental Science', 'Environmental Science', '2017-09-01', '2020-06-30', 'Explored topics such as ecology, environmental policy, conservation biology, and sustainable development principles.'),
(12, 4, 'IT Training Center', 'Cisco Certified Network Associate (CCNA)', 'Network Engineering', '2016-07-01', '2017-12-15', 'Acquired knowledge and skills in network fundamentals, routing and switching, network security, and troubleshooting.'),
(13, 7, 'Research University', 'Ph.D. in Computer Science', 'Computer Science', '2015-09-01', '2020-12-20', 'Conducted research in artificial intelligence, machine learning, natural language processing, and human-computer interaction.'),
(14, 13, 'Product Management Institute', 'Certificate in Product Management', 'Product Management', '2017-10-05', '2018-11-30', 'Learned about product lifecycle management, market analysis, product strategy, and agile development methodologies.'),
(15, 15, 'IT Certification Center', 'Microsoft Certified Systems Administrator (MCSA)', 'Information Technology', '2016-08-01', '2017-11-30', 'Gained expertise in Microsoft Windows server administration, network infrastructure configuration, and system troubleshooting techniques.');

-- --------------------------------------------------------

--
-- Table structure for table `t_offre_emploi`
--

CREATE TABLE `t_offre_emploi` (
  `ID_Offre` int(11) NOT NULL,
  `FK_Employeur` int(11) NOT NULL,
  `Titre` varchar(255) NOT NULL,
  `Description` text NOT NULL,
  `Date_Publication` date NOT NULL,
  `Date_Expiration` date DEFAULT NULL,
  `Type_Contrat` varchar(50) DEFAULT NULL,
  `Localisation` varchar(255) DEFAULT NULL,
  `Salaire` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `t_offre_emploi`
--

INSERT INTO `t_offre_emploi` (`ID_Offre`, `FK_Employeur`, `Titre`, `Description`, `Date_Publication`, `Date_Expiration`, `Type_Contrat`, `Localisation`, `Salaire`) VALUES
(1, 3, 'Senior Software Engineer', 'We are seeking a talented Senior Software Engineer to join our dynamic team. The ideal candidate will have a strong background in software development and a passion for innovation.', '2024-03-01', '2024-04-01', 'Full-time', 'Cityville', 0.00),
(2, 8, 'Financial Analyst', 'Global Finance Group is looking for a skilled Financial Analyst to support our finance team. The candidate should have strong analytical skills and a solid understanding of financial principles.', '2024-02-20', '2024-03-20', 'Full-time', 'Townsville', 0.00),
(3, 1, 'Software Developer', 'HealthTech Solutions is hiring a Software Developer to work on innovative healthcare software solutions. The candidate should be proficient in programming languages and have experience in healthcare IT.', '2024-02-15', '2024-03-15', 'Full-time', 'Villageton', 0.00),
(4, 6, 'Digital Marketing Manager', 'Join our team at Marketing Pro Agency as a Digital Marketing Manager. We are looking for someone with expertise in digital marketing strategies and a track record of driving results.', '2024-03-05', '2024-04-05', 'Full-time', 'Suburbia', 0.00),
(5, 12, 'Management Consultant', 'Consulting Solutions LLC is seeking a Management Consultant to provide strategic consulting services to our clients. The ideal candidate should have strong problem-solving skills and experience in business consulting.', '2024-02-25', '2024-03-25', 'Full-time', 'Countryside', 0.00),
(6, 9, 'Graphic Designer', 'Creative Design Studio is looking for a talented Graphic Designer to create visually stunning designs for our clients. The candidate should be creative, detail-oriented, and proficient in graphic design software.', '2024-03-10', '2024-04-10', 'Full-time', 'Cityside', 0.00),
(7, 5, 'Supply Chain Manager', 'Logistics Solutions Inc. is hiring a Supply Chain Manager to oversee our supply chain operations. The ideal candidate should have strong leadership skills and experience in logistics and inventory management.', '2024-02-18', '2024-03-18', 'Full-time', 'Metropolis', 0.00),
(8, 11, 'Venture Capital Analyst', 'TechStart Ventures is seeking a Venture Capital Analyst to evaluate investment opportunities in technology startups. The candidate should have strong financial analysis skills and a passion for technology.', '2024-03-02', '2024-04-02', 'Full-time', 'Townsville', 0.00),
(9, 10, 'Project Manager', 'Join Construction Dynamics as a Project Manager and oversee construction projects from inception to completion. The candidate should have strong project management skills and experience in construction.', '2024-02-28', '2024-03-28', 'Full-time', 'Villageton', 0.00),
(10, 2, 'Research Analyst', 'Healthcare Innovations Group is hiring a Research Analyst to conduct research on healthcare trends and technologies. The candidate should have strong analytical skills and a background in healthcare research.', '2024-03-08', '2024-04-08', 'Full-time', 'Suburbia', 0.00),
(11, 14, 'Environmental Consultant', 'EcoFriendly Solutions is seeking an Environmental Consultant to provide environmental consulting services. The candidate should have knowledge of environmental regulations and experience in environmental science.', '2024-03-12', '2024-04-12', 'Full-time', 'Hamletown', 0.00),
(12, 4, 'Systems Engineer', 'TechCorp Industries is hiring a Systems Engineer to design and implement IT systems and infrastructure solutions. The candidate should have strong technical skills and experience in system administration.', '2024-02-22', '2024-03-22', 'Full-time', 'Countryside', 0.00),
(13, 7, 'Research Scientist', 'Join InnovateX Inc. as a Research Scientist and contribute to cutting-edge research and development projects. The candidate should have a Ph.D. in a related field and experience in research.', '2024-03-15', '2024-04-15', 'Full-time', 'Cityside', 0.00),
(14, 13, 'Product Manager', 'Global Healthcare Solutions is seeking a Product Manager to manage the development and launch of healthcare software products. The candidate should have strong product management skills and a background in healthcare IT.', '2024-02-29', '2024-03-29', 'Full-time', 'Metropolis', 0.00),
(15, 15, 'Systems Administrator', 'Tech Innovations Inc. is hiring a Systems Administrator to administer and maintain IT systems and infrastructure. The candidate should have strong technical skills and experience in system administration.', '2024-03-20', '2024-04-20', 'Full-time', 'Hamletown', 0.00);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `t_candidat`
--
ALTER TABLE `t_candidat`
  ADD PRIMARY KEY (`ID_Candidat`),
  ADD UNIQUE KEY `Email` (`Email`);

--
-- Indexes for table `t_candidature`
--
ALTER TABLE `t_candidature`
  ADD PRIMARY KEY (`ID_Candidature`),
  ADD KEY `FK_Candidat` (`FK_Candidat`),
  ADD KEY `FK_Offre` (`FK_Offre`);

--
-- Indexes for table `t_competence`
--
ALTER TABLE `t_competence`
  ADD PRIMARY KEY (`ID_Competence`);

--
-- Indexes for table `t_competences_candidat`
--
ALTER TABLE `t_competences_candidat`
  ADD PRIMARY KEY (`FK_Candidat`,`FK_Competence`),
  ADD KEY `FK_Competence` (`FK_Competence`);

--
-- Indexes for table `t_employeur`
--
ALTER TABLE `t_employeur`
  ADD PRIMARY KEY (`ID_Employeur`),
  ADD UNIQUE KEY `Email` (`Email`);

--
-- Indexes for table `t_experience_professionnelle`
--
ALTER TABLE `t_experience_professionnelle`
  ADD PRIMARY KEY (`ID_Experience`),
  ADD KEY `FK_Candidat` (`FK_Candidat`);

--
-- Indexes for table `t_formation`
--
ALTER TABLE `t_formation`
  ADD PRIMARY KEY (`ID_Formation`),
  ADD KEY `FK_Candidat` (`FK_Candidat`);

--
-- Indexes for table `t_offre_emploi`
--
ALTER TABLE `t_offre_emploi`
  ADD PRIMARY KEY (`ID_Offre`),
  ADD KEY `FK_Employeur` (`FK_Employeur`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `t_candidat`
--
ALTER TABLE `t_candidat`
  MODIFY `ID_Candidat` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `t_candidature`
--
ALTER TABLE `t_candidature`
  MODIFY `ID_Candidature` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `t_competence`
--
ALTER TABLE `t_competence`
  MODIFY `ID_Competence` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `t_employeur`
--
ALTER TABLE `t_employeur`
  MODIFY `ID_Employeur` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `t_experience_professionnelle`
--
ALTER TABLE `t_experience_professionnelle`
  MODIFY `ID_Experience` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `t_formation`
--
ALTER TABLE `t_formation`
  MODIFY `ID_Formation` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `t_offre_emploi`
--
ALTER TABLE `t_offre_emploi`
  MODIFY `ID_Offre` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `t_candidature`
--
ALTER TABLE `t_candidature`
  ADD CONSTRAINT `t_candidature_ibfk_1` FOREIGN KEY (`FK_Candidat`) REFERENCES `t_candidat` (`ID_Candidat`) ON DELETE CASCADE,
  ADD CONSTRAINT `t_candidature_ibfk_2` FOREIGN KEY (`FK_Offre`) REFERENCES `t_offre_emploi` (`ID_Offre`) ON DELETE CASCADE;

--
-- Constraints for table `t_competences_candidat`
--
ALTER TABLE `t_competences_candidat`
  ADD CONSTRAINT `t_competences_candidat_ibfk_1` FOREIGN KEY (`FK_Candidat`) REFERENCES `t_candidat` (`ID_Candidat`) ON DELETE CASCADE,
  ADD CONSTRAINT `t_competences_candidat_ibfk_2` FOREIGN KEY (`FK_Competence`) REFERENCES `t_competence` (`ID_Competence`) ON DELETE CASCADE;

--
-- Constraints for table `t_experience_professionnelle`
--
ALTER TABLE `t_experience_professionnelle`
  ADD CONSTRAINT `t_experience_professionnelle_ibfk_1` FOREIGN KEY (`FK_Candidat`) REFERENCES `t_candidat` (`ID_Candidat`) ON DELETE CASCADE;

--
-- Constraints for table `t_formation`
--
ALTER TABLE `t_formation`
  ADD CONSTRAINT `t_formation_ibfk_1` FOREIGN KEY (`FK_Candidat`) REFERENCES `t_candidat` (`ID_Candidat`) ON DELETE CASCADE;

--
-- Constraints for table `t_offre_emploi`
--
ALTER TABLE `t_offre_emploi`
  ADD CONSTRAINT `t_offre_emploi_ibfk_1` FOREIGN KEY (`FK_Employeur`) REFERENCES `t_employeur` (`ID_Employeur`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
