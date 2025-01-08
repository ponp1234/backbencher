from app import db, Question, Exam, app  # Import app and models from your main application
# Example exam title to delete and recreate
exam_title = "P3 science-gojs"

with app.app_context():
    # Check if the exam already exists and delete it along with its questions
    exam = Exam.query.filter_by(title=exam_title).first()
    if exam:
        # Delete associated questions
        Question.query.filter_by(exam_id=exam.id).delete()
        # Delete the exam itself
        db.session.delete(exam)
        db.session.commit()  # Commit the deletion

    # Recreate the exam
    new_exam = Exam(title=exam_title)
    db.session.add(new_exam)
    db.session.commit()  # Commit to get the new exam ID



    # Question with a GoJS diagram
    questions = [
        {
            "question_text": """
                <div>
                    <p>The diagram below shows the interaction between different components. Identify the correct relationship:</p>
                    <div id="gojs-diagram" style="width:400px; height:300px; background-color: #F3F3F3;"></div>
                    <script>
                        function init() {
                            const $ = go.GraphObject.make;  // for conciseness in defining templates
                            const diagram = $(go.Diagram, "gojs-diagram", {
                                initialAutoScale: go.Diagram.Uniform,  // scale diagram to fit viewport
                                layout: $(go.TreeLayout)  // use a tree layout
                            });
    
                            diagram.nodeTemplate =
                                $(go.Node, "Horizontal",
                                    $(go.TextBlock,
                                        { margin: 8 },
                                        new go.Binding("text", "key"))
                                );
    
                            diagram.model = new go.TreeModel([
                                { key: "A" },
                                { key: "B", parent: "A" },
                                { key: "C", parent: "A" },
                                { key: "D", parent: "B" }
                            ]);
                        }
                        window.addEventListener('load', init);
                    </script>
                </div>
            """,
            "option_a": "Relationship A",
            "option_b": "Relationship B",
            "option_c": "Relationship C",
            "option_d": "Relationship D",
            "correct_option": "option_c",  # Replace with the correct option
            "question_type": "single"
        },
        {
                "question_text": """
                    <div>
                        <p>The chart below shows the interaction between different components. Identify the correct relationship:</p>
                        <div id="echarts-diagram" style="width:400px; height:300px;"></div>
                        <script src="https://cdn.jsdelivr.net/npm/echarts/dist/echarts.min.js"></script>
                        <script>
                            document.addEventListener("DOMContentLoaded", function () {
                                const chartDom = document.getElementById('echarts-diagram');
                                const myChart = echarts.init(chartDom);
                                const option = {
                                    title: {
                                        text: 'Component Interaction',
                                        left: 'center',
                                    },
                                    tooltip: {
                                        trigger: 'item',
                                    },
                                    series: [
                                        {
                                            type: 'tree',
                                            data: [
                                                {
                                                    name: 'A',
                                                    children: [
                                                        {
                                                            name: 'B',
                                                            children: [
                                                                { name: 'D' },
                                                            ],
                                                        },
                                                        { name: 'C' },
                                                    ],
                                                },
                                            ],
                                            top: '10%',
                                            left: '15%',
                                            bottom: '10%',
                                            right: '15%',
                                            symbolSize: 12,
                                            label: {
                                                position: 'top',
                                                verticalAlign: 'middle',
                                                align: 'right',
                                                fontSize: 12,
                                            },
                                            leaves: {
                                                label: {
                                                    position: 'top',
                                                    verticalAlign: 'middle',
                                                    align: 'left',
                                                },
                                            },
                                            emphasis: {
                                                focus: 'descendant',
                                            },
                                            expandAndCollapse: true,
                                            animationDuration: 750,
                                            animationEasing: 'cubicOut',
                                        },
                                    ],
                                };
                                myChart.setOption(option);
                            });
                        </script>
                    </div>
                """,
                "option_a": "Relationship A",
                "option_b": "Relationship B",
                "option_c": "Relationship C",
                "option_d": "Relationship D",
                "correct_option": "option_c",  # Replace with the correct option
                "question_type": "single"
            }        
    ]
    
    # Add questions to the database with the new exam ID
    for q in questions:
        question = Question(
            exam_id=new_exam.id,
            question_text=q["question_text"],
            option_a=q.get("option_a"),
            option_b=q.get("option_b"),
            option_c=q.get("option_c"),
            option_d=q.get("option_d"),
            correct_option=q.get("correct_option"),
            question_type=q["question_type"]
        )
        db.session.add(question)
    
    db.session.commit()
    print("Exam and questions added successfully.")

