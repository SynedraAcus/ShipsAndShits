#  Script(s) for node events. Each node starts with label node[\d][\d]?\:

label node1:
    label node1_event1:
        nvl clear
        "Вы наблюдаете событие №1, имеющее вероятность 10\%"
        jump node1_quit
    label node1_event2:
        nvl clear
        "Вы наблюдаете событие №2, имеющее вероятность 20\%"
        jump node1_quit
    label node1_event3:
        nvl clear
        "Вы наблюдаете событие №3, имеющее вероятность 20\%"
    label node1_quit:
        show screen map_screen

label node2:
    nvl clear
    label node2_quit:
        show screen map_screen

label node3:
    nvl clear
    label node3_quit:
        show screen map_screen

label node4:
    nvl clear
    label node4_quit:
        show screen map_screen

label node5:
    nvl clear
    label node5_quit:
        show screen map_screen

label node6:
    nvl clear
    label node6_quit:
        show screen map_screen

label node7:
    nvl clear
    label node7_quit:
        show screen map_screen

label node8:
    nvl clear
    label node8_quit:
        show screen map_screen

label node9:
    label node9_quit:
        show screen map_screen

label node10:
    nvl clear
    label node10_quit:
        show screen map_screen

label node11:
    nvl clear
    label node11_quit:
        show screen map_screen

label node12:
    nvl clear
    label node12_quit:
        show screen map_screen

label node13:
    nvl clear
    label node13_quit:
        show screen map_screen

label node14:
    nvl clear
    label node14_lost_in_sea:
        "В этот раз Безмятежность, кажется, решила дать людям передышку и посоответствовать немного своему названию. Ни волн, превышающих в размере самую высокую вашу мачту, ни подводных течений, угрожающих пробить дыру где-нибудь под килем, ни ветра, срывающего паруса."
        " — Одно удовольствие ходить по такому морю, а, капитан? — не скрывая восторга, делится переживаниями рулевой. Впрочем, его восторг оказывается преждевременным: на горизонте - и к, сожалению, точно по курсу - вы замечаете нечто, больше всего похожее на колеблющийся столб, уходящий в небеса. Рулевой поворачивает голову вслед за вашим взглядом и бранится, не стесняясь в выражениях."
        " — Я сверился с картой течений. Если мы не хотим попробовать на вкус песок у подножия горы Пуп - придётся держать курс. — обрисовывает ситуацию вставший рядом старпом."
        menu:
            "Держаться заданного курса":
                "Вы приободряете рулевого и приказываете идти прямо на столб. Примерно так и начиналась половина историй вашего батюшки, и видит бог, то были отличные истории. Старпом чуть заметно кивает, следит некоторое время за приближающимся столбом, а затем уходит объяснять ситуацию команде."
                nvl clear
                "Наконец вы приближаетесь к столбу на расстояние, достаточное для осмотра, и останавливаетесь. Становится ясно, что никакой это не столб - это, скорее, гигантская спираль, разворачивающаяся сверху в клубящуюся светлую тучу. Она не движется - только тихонько раскачивается из стороны в сторону."
                " — Значит, ураган, — говорит старпом. Его лицо будто не знает, как себя вести: поперек лба пролегла глубокая морщина, морщинки поменьше появились в уголках глаз и рта, но глаза только что не мечут искры."
                menu:
                    "Спросить о смысле сказанного":
                        nvl clear
                        " — Климатическое явление, появляющееся в наших краях достаточно редко, чтобы стать легендарным. Ураган несется по суше и морю, подхватывая всё, что попадется ему на пути, а в один момент рассыпается безо всякой видимой причины. Старые говорят, что ураган - самый быстрый путь в Небесную Республику... или на дно морское. — Старпом замолкает и вглядывается в будто кипящую от постоянного движения воду."
                        " — Бабка рассказывала, что ураган — это молодое любопытное облако, которое спустилось вниз, чтобы всё посмотреть. Вроде как познакомиться с миром. Но я всегда думал, что это байка для маленьких, — шмыгнув для уверенности носом, добавляет выбравшийся на палубу юнга, во все глаза уставившийся на столб."
                        " — Поговаривают, что где-то за Львовыми Озерами ураганы приручили и катаются на них так же, как мы — на омутном осьминоге. — Вносит свою лепту в разговор неизвестно откуда появившийся кок. Оглянувшись, вы обнаруживаете, что посмотреть на диковинный каприз природы пришла по меньшей мере половина команды, и, подождав немного, гоните их по местам."
                        "Ворча, команда расходится и принимается готовиться к грядущему. Кажется, они думают, что вы прикажете нырять прямо в ураган."
                        $ player_deck.append(Card(u'З', 3, spendable = True, tooltip = u'История, рассказанная членами вашей команды'))
                        label lost_in_sea_choose:
                        menu:
                            "Узнать мнение старпома" if "firstofficer" in node_lost_in_sea_interview:
                                nvl clear
                                "Старпом будто и не слышал предыдущего вашего приказа. Он стоит в той же позе, опершись о борт, и сверлит глазами ураган. Кажется, это первый раз, когда вы видите его ссутулившимся. Вы подходите ближе и негромко спрашиваете, что он думает по этому поводу."
                                " — Я никогда не верил в сказки, капитан. Ураган, скорее всего, просто разобьет наш корабль о скалы, если нас всех не смоет за борт еще до этого."
                                "Вы не отвечаете, когда старпом замолкает. После паузы он продолжает:"
                                " — Вы не боитесь однажды проснуться, заглянуть в зеркало и понять: эта старая, обрюзгшая, тошнотворная рожа - действительно ваша? И останется вашей, и вам придётся к ней привыкнуть, и расколотить все зеркала в доме, потому что невозможно смотреть на неё каждый божий день."
                                "Старпом складывает руки на груди и наконец выпрямляется."
                                " — Отдайте приказ. Привяжем всё ценное, обвяжемся сами, помолимся и поплывем прямо в ураган - только прикажите сохранять курс. — Старпом неловко дергает плечами, разворачивается, говорит, что пойдет осмотрит груз и уходит. Вы смотрите ему вслед, а затем поворачиваетесь обратно к смерчу."
                                $ node_lost_in_sea_interview.remove("firstofficer")
                                jump lost_in_sea_choose
                            "Пройтись по кораблю" if "walkthrough" in node_lost_in_sea_interview:
                                nvl clear
                                "Вы отправляетесь прогуляться по судну: узнать, в каком состоянии корабль и что думают остальные члены команды. Осмотрев паруса (они на месте), вы спускаетесь в камбуз в надежде разузнать у кока что-нибудь о способах приручения ураганов. В камбузе, впрочем, кока не обнаруживается: только юнга сидит на ящике и гипнотизирует лежащие на столе картошку и нож. Вы здороваетесь и спрашиваете, как жизнь."
                                " — Хорошо. Только, кажется, мало, — Юнга робко улыбается. У него самую чуточку дрожат руки. Наконец, он собирается с мыслями и проговаривает, глядя на балки над вашей головой:"
                                " — Капитан, я пойду за вами куда угодно. Только, ну, давайте никуда не пойдем? Я спрашивал у рулевого, мы можем проплыть мимо и идти своей дорогой. Нам совсем незачем брать штурмом небо, как по мне."
                                "Его перебивает вошедший кок. Он аккуратно отодвигает вас в сторону внушительным животом и громогласно вопрошает, что за капитуляция происходит в вверенном ему помещении. Затем он замечает вас, здоровается и сообщает:"
                                nvl clear
                                " — А я только от матросов. Они попросили меня заранее провести над ними необходимые обряды, раз уж мы, возможно, отправляемся на верную смерть. Я ведь, вообще-то, священник Монастыря с полной подготовкой и не виноват, что никто не этой посудине не умеет готовить. Между прочим, мне полагается двойная ставка, и я намерен..."
                                "Вы прекрасно знаете, насколько этот разговор может затянуться: кок - человек неимоверно словоохотливый, так что довольно бесцеремонно перебиваете его речь вопросом об упомянутых им традициях за Львовыми Озерами."
                                " — А, это. Ну, откровенно говоря, я даже не уверен, что где-то существует место с таким названием. Нужно было срочно сказать что-то, что не испугает всех еще больше после слов нашего милашки-старпома, вот я и ляпнул первое, что пришло на ум. — Юнга судорожно вздыхает и съёживается. Кок меж тем требовательно смотрит на вас."
                                " — Так что, капитан? Я не зря потратил полчаса, вспоминая подходящие случаю молитвы, или мы всё-таки не лезем к чёрту в зубы?"
                                "Вместо ответа вы зовёте его с собой на палубу: объявление в любом случае нужно сделать всем."
                                $ node_lost_in_sea_interview.remove("walkthrough")
                                jump lost_in_sea_choose
                            "Принять решение":
                                nvl clear
                                "Вы какое-то время ждёте, и палуба начинает наполняться людьми. Кажется, весь экипаж собрался здесь, чтобы узнать, как сложится их дальнейшая судьба. К вам подходит грузный, трудноопределяемого возраста боцман и сообщает, что трюмы подготовлены к заходу в ураган по мере его возможностей и, не дожидаясь ответа, возвращается на место. Рулевой несколько дурашливо отдаёт честь и от лица матросов говорит, что они настроены исполнять приказы, какими бы они не были. Юнга, по обыкновению своему свисающий с одной из мачт, смотрит на вас умоляюще - насколько это возможно из перевернутого положения. Кажется, настала пора что-то решать."
                                menu:
                                    "Плыть в ураган":
                                        "Кажется, большая часть команды готовилась именно к этому. Они напуганы, конечно, они чертовски напуганы, но они пойдут за вами, если это необходимо. Вы кратко раздаёте приказы, и вокруг закипает жизнь: сворачиваются паруса, закрепляются последние ящики, моряки занимают места у весел. Вы подходите к мачте, треплете дрожащего юнгу по голове и вместе спускаете флаг. Наконец, всё готово - насколько такой корабль, как ваш, может быть готов к подобному приключению."
                                        menu:
                                            "Вперёд!":
                                                nvl clear
                                                "Ритмичный плеск воды, скрип уключин, свист урагана. Вы медленно, но верно приближаетесь к тому, что всегда было не самой правдоподобной байкой. Затянувшееся молчание прерывает медленно нарастающий гул голосов, повторяющих одни и те же слова."
                                                " — Игидай, Игидай, игги-дигги-дай-до, Игидай, Игидай, игги-дигги-дай-до, игги-дигги-до! — раз за разом, снова и снова. Это поют моряки, налегая на весла в такт песне. Кажется, теперь эти слова будут разноситься по кораблю до самого конца."
                                                "Корабль движется всё быстрее и быстрее, и это не дело рук гребцов. Чем ближе вы подходите к урагану, тем сильнее он притягивает вас к себе, и в какой-то момент моряки совсем бросают весла - но почему-то не прекращают петь."
                                                " — Игидай, Игидай, игги-дигги-дай-до, Игидай, Игидай, игги-дигги-дай-до, игги-дигги-до, игги-дай, Игидай-дай-до, Игидай! — теперь, без аккомпанемента весел, песня всё больше рассыпается на отдельные фразы - будто каждый из моряков придумывает свои незамысловатые строчки на ходу. Ваш корабль неожиданно бесшумно отрывается от поверхности воды: только с плеском падает вниз плохо закрепленное весло. Вы помогаете старпому привязаться к мачте, хотя безопаснее было бы уйти в трюмы, и спешно привязываетесь сами."
                                                " — Как красиво! Может, всё это время нам стоило молиться небу, а не морю, как вы думаете, капитан? — щурится и смеётся старпом, а потом вас хватает ураган, и становится ясно, что теперь ваша судьба зависит только от слепого случая. Игги-дигги-до!"
                                                $ how_about_miracle = renpy.random.choice(['miracle', 'no_miracle'])
                                                if how_about_miracle == "no_miracle":
                                                    nvl clear
                                                    "Корабль несется вверх по спирали, крутясь и кувыркаясь, давно лишившись мачт и парусов, а вы успеваете только удивляться тому, что еще не захлебнулись. Затем вас будто выплевывает наверх, и вы избитым килем седлаете облако, только чтобы обнаружить, что всё, совершенно всё, что вам рассказывали о мире - правда. Вы видите, как опускаются над Востоком-за-Океаном два солнца, и слышите пение прозрачных, невесомых птиц - они выкапывают себе гнезда в облаках и деловито выбивают из них дождь. Бесконечные караваны на самом деле шагают к оазисам песчаного короля и действительно существует скала, отбрасывающая тень на целую страну. Мир существует. Мир правда существует."
                                                    " — Капитан! А ведь наше море и правда зеленое! А я никогда не верил, думал, что у приезжих просто глаза неправильно устроены, — делится переживаниями юнга, выбравшийся наконец на палубу. Хорошо, что он больше не боится. Вы глядите вниз, на и в самом деле зеленоватую воду, и это будто выключает что-то очень важное: ураган втягивает вас обратно и закручивает эту карусель еще раз."
                                                    "Пискнув, юнга обвивает всеми конечностями остатки мачты, и это последнее, что вы видите перед прыжком в бурлящую стену. Ураган забавляется с вами, будто с игрушкой, и печальный хруст древесины вы слышите всё чаще. Наконец облако срывается с вершины урагана, и водяной столб, бывший его основой, рассыпается на волны и капли. То, что осталось от вашего корабля, летит вниз вместе с ними и, по иронии судьбы, вы разбиваетесь о зубы Пупа. Обломки дерева и обрывки парусов усеивают теперь береговые скалы, а солёные реки, подпитывающие море, на время изменят исток: великан выбрался из своей пещеры, чтобы оплакать новую жертву Безмятежности."
                                                    nvl clear
                                                    "Прощайте, капитан. Вашу историю было приятно рассказать."
                                                    return
                                                if how_about_miracle == "miracle":
                                                    nvl clear
                                                    "Вы запомнили не так уж много: в основном попытки не захлебнуться и постоянные, тошнотворные перемены высоты, и болезненный хруст мачт, и сорвавшегося моряка. А затем вас взмыло на самый верх, внутрь облака, и вы видели, как солнце заливает степи Тартари, как плывут по разливам Столицы кажущиеся миниатюрными кораблики, как великан, заинтригованный шумом проносящегося рядом урагана, выглядывает из своей пещеры и улыбается вам, размазывая слезы по огромному лицу, и заблудившийся альбатрос успевает сесть на то, что осталось от вашей реи, пока ураган не втягивает вас снова, закручивая сильнее и быстрее, чем когда-либо."
                                                    "В те редкие минуты, когда вы примерно представляете, что происходит, вы чувствуете движение. Вас не просто швыряет от края к краю урагана, вы летите вместе с ним. Трудно определить, сколько прошло времени: иногда вам кажется, что вы провели в воздухе не больше десяти минут, а иногда - что крутитесь здесь уже много часов. Наконец болтанка начинает затихать, и вы чувствуете, что снижаетесь - не плавно, рывками, но всё же снижаетесь. С прощальным плеском ураган рассыпается, когда вы уже зависли над водной гладью, и корабль тяжело скрипит, погружаясь куда выше ватерлинии. Постепенно на палубу, кряхтя и стеная, выбирается ваша команда. Юнга приходит в себя первым и подбегает к борту, перегибается и глядит на воду."
                                                    " — Вода какая-то... не такая, — озадаченно заключает юнга после тщательного осмотра и вы подходите к борту сами."
                                                    "Вода и правда не такая. Она синяя. Гораздо более синяя, чем вы привыкли видеть. Вы оглядываетесь по сторонам: у островов на горизонте не те очертания, у теней, шныряющих в воде, не те движения, а горы, на которую ориентируется всякий идущий в Вейн, нет вовсе."
                                                    nvl clear
                                                    " — Что ж, я думаю, мы можем поискать Львовые Озера здесь. Не мог же я сам придумать такое дурацкое название! — зубоскалит кок, но, несмотря на браваду, он ошарашен не меньше остальных. Пока команда прыгает от борта к борту и делится друг с другом самыми впечатляющими подробностями места, куда вы попали, к вам подходит старпом - прямой и снова застегнутый на все пуговицы. Он кратко, без объяснений благодарит вас и советует поскорее достичь суши: долго ваш кораблик не протянет. Вы киваете и охрипшим от волнения голосом приказываете прекратить балаган, садиться на весла и плыть к островам, где горит маяк, сверкающий даже сейчас, при свете солнца. Моряки встречают приказ радостным гулом и рассаживаются по местам. Теперь их песня - а они заводят её снова - звучит иначе, торжествующе и благодарно одновременно. Вы сами встаёте к рулю, юнга мчится поднимать флаг, а рулевой, посмотрев на вас и пожав плечами, плюхается на пол и смотрит в незнакомое небо."
                                                    "До встречи, капитан. Надеюсь, мы о вас еще услышим."
                                                    return

                                    "Отправиться своей дорогой":
                                        "Кое-кто, желая показаться храбрее, чем они есть, кривят лица, но вы ясно слышите вздох облегчения, пронесшийся над толпой. Вы тщательно зарисовываете ураган и записываете его поведение: такие новости определенно вызовут интерес у определенного круга лиц. Закончив, вы трогаете рулевого за плечо, и он, согласно кивнув, крутит штурвал. Пора продолжать путь."
                                        $ gl_cargo.append("hurricane_blueprints")
                                        show screen map_screen
                    "Не отвечая, развернуться и поплыть наугад":
                        jump lost_in_sea_runaway
            "Свернуть и надеяться на лучшее":
                label lost_in_sea_runaway:
                nvl clear
                "К черту всё. В конце концов, вы хотя бы знаете, чего можно ждать от Безмятежности. Ожидать же чего-то от невероятного столба из моря - попросту глупо. Мама говорила, что вы удачливы от природы: пора это проверить. Вы отдаёте необходимые приказы, следите, как спускают паруса и собственноручно гоните команду прочь с палубы. Наконец, приготовления закончены, и вы поворачиваете руль, не заботясь особенно о точности: кровожадное море сделает всё само."
                "Безмятежность действительно милосердна сегодня. После краткой, но яростной гонки вы сравнительно мягко причаливаете к берегу Риторического. Отсюда можно продолжать плыть в сравнительной безопасности."
                $ current_port = poop
                jump node14_quit
    label node14_quit:
        show screen map_screen

label node15:
    nvl clear
    label node15_quit:
        show screen map_screen

label node16:
    nvl clear
    label node16_quit:
        show screen map_screen

label node17:
    nvl clear
    label node17_quit:
        show screen map_screen

label node18:
    nvl clear
    label node18_quit:
        show screen map_screen

label node19:
    nvl clear
    label node19_quit:
        show screen map_screen

label node20:
    nvl clear
    label node20_quit:
        show screen map_screen
    "NOTHING"