class Token:
    def __init__(self, new_token_id, old_token_id, uri):
        self.new_token_id = new_token_id
        self.old_token_id = old_token_id
        self.uri = uri

class Environment:
    def __init__(self, old_token, opensea_proxy, tokens):
        self.old_token = old_token
        self.opensea_proxy = opensea_proxy
        self.tokens = tokens

polygon = Environment(
    old_token = "0x2953399124f0cbb46d2cbacd8a89cf0599974963",
    opensea_proxy = "0x58807baD0B376efc12F5AD86aAc70E78ed67deaE",
    tokens = [
        Token(1, 10110860822564241239994147652924744222037427536707093556420917645282000240641, "bafkreiadflw5nc747gf2vxn6sw5kkit5mef7sn4agx6pdhfmn7c6ahlfmy"),
        Token(2, 10110860822564241239994147652924744222037427536707093556420917646381511868417, "bafkreib44oinppf323da3lnwiad6lerojeflp6szg3o4jakzr6amjfap24"),
        Token(3, 10110860822564241239994147652924744222037427536707093556420917647481023496193, "bafkreiaxhonid7657jme64dutevow4wjpmkxuiurlxo2xlo2yeisy6kika"),
        Token(4, 10110860822564241239994147652924744222037427536707093556420917648580535123969, "bafkreifhnw6vaxr5pidw4lyn3hyfxds4et46u2o4buvila42n475xb3u2i"),
        Token(5, 10110860822564241239994147652924744222037427536707093556420917650779558379521, "bafkreifyu74c4l7igamdynktbynh3tw37vpgse65mzcfw7s2by52kaqe6y"),
        Token(6, 10110860822564241239994147652924744222037427536707093556420917651879070007297, "bafkreibhdoiw4sr5le7cuex6zshr6ghcscqs65hntckdlrutchqlarpwme"),
        Token(7, 10110860822564241239994147652924744222037427536707093556420917652978581635073, "bafkreig6liief2be6fsh4fj4j3sjx443sr7a6nwqkmlmfladkadnhvo4oa"),
        Token(8, 10110860822564241239994147652924744222037427536707093556420917654078093262849, "bafkreieq3mremf3ezg23p3mh4v2nytwurpkxnamutiga6vxl4i74k6qy5e"),
        Token(9, 10110860822564241239994147652924744222037427536707093556420917655177604890625, "bafkreifagd7j3zmtxk5coeirs4fcoknn75q6mnjs2cnrfa2dxm3mnnqhpa"),
        Token(10, 10110860822564241239994147652924744222037427536707093556420917656277116518401, "bafkreihpl325gxv3srjpidlirojc7jllyxalg2o63ywmqjsxmc755k7qfu"),
        Token(11, 10110860822564241239994147652924744222037427536707093556420917657376628146177, "bafkreidjbyiggganu2bpl5gaqoy5baj5eowolmtffpzmfs62yo3oiubuga"),
        Token(12, 10110860822564241239994147652924744222037427536707093556420917658476139773953, "bafkreif4kw2wmfqqreleghkwgxrk65bjuraliwpb6fsox2rkcgey4eauvu"),
        Token(13, 10110860822564241239994147652924744222037427536707093556420917659575651401729, "bafkreiaw3weanle76h7fk6wq6gkwcwm4xkuargmnczslmrk3asdsxguzta"),
        Token(14, 10110860822564241239994147652924744222037427536707093556420917660675163029505, "bafkreiakj4gkwkuxmtcackjdlzs7pcnnogbsk4wgou2o5btcuxtqc75u2e"),
        Token(15, 10110860822564241239994147652924744222037427536707093556420917661774674657281, "bafkreigbukn6einpc3m3uhk3ejs3t3smh63o527oe7s7pd6xsa6dcjfiti"),
        Token(16, 10110860822564241239994147652924744222037427536707093556420917662874186285057, "bafkreigvjhehvnn55kjdhvuxnclejg2ntczaare6h73c3n5o2rnvpw2yau"),
        Token(17, 10110860822564241239994147652924744222037427536707093556420917663973697912833, "bafkreiemax3g4cflwhicboshmtgdmkrrjwskhfhhjstraamw3lf2evb7bu"),
        Token(18, 10110860822564241239994147652924744222037427536707093556420917665073209540609, "bafkreicmskvgk4x2xfzvgad64q6mprh4fckuevbrgr62dygvyctaymbcxm"),
        Token(19, 10110860822564241239994147652924744222037427536707093556420917666172721168385, "bafkreiayw2vnvct4uewfh6gayniqklpcegdywr7v555v2fkggc5shvysu4"),
        Token(20, 10110860822564241239994147652924744222037427536707093556420917667272232796161, "bafkreig7dwqz4ylezvsnmhowclsw2h3amkwimt6pg6bzmbmzou54r4kd3i"),
        Token(21, 10110860822564241239994147652924744222037427536707093556420917668371744423937, "bafkreicdswtlrwxyrxer6vo6q7acavopvjk2ruxds2qkpwwol7akxdxn4u"),
        Token(22, 10110860822564241239994147652924744222037427536707093556420917669471256051713, "bafkreigjthhl6lk5bgyeggkvqtsn6jnb73wznh6hpefw7mc5ldfhkfdl4e"),
        Token(23, 10110860822564241239994147652924744222037427536707093556420917670570767679489, "bafkreid2xkvt34nomytuhkqcw76auc25dso6ceub2w3op27yfw7u5derxi"),
        Token(24, 10110860822564241239994147652924744222037427536707093556420917671670279307265, "bafkreifqmbmff3chalfsvn55e6r2bjouux4rf7hdvxepcjl22hg7uaeijq"),
        Token(25, 10110860822564241239994147652924744222037427536707093556420917672769790935041, "bafkreievyfuotjfaonejsji3e4hd6w5txx2jthqtbpgpnwp6lhhfh5dtk4"),
        Token(26, 10110860822564241239994147652924744222037427536707093556420917673869302562817, "bafkreigw6wzptyg7qn5o43nw5fs4nav2j2h2wolddxrb4ootwm6zd3a7g4"),
        Token(27, 10110860822564241239994147652924744222037427536707093556420917674968814190593, "bafkreidhntcj5c6piool2dcg5h7hlwc5hulkkjsgrb32lpls5jfrfskqsy"),
        Token(28, 10110860822564241239994147652924744222037427536707093556420917676068325818369, "bafkreicct4dpexih5lb6kg5snxcsj7vf7uirovj2imntxxa2km73rr3twy"),
        Token(29, 10110860822564241239994147652924744222037427536707093556420917677167837446145, "bafkreian4j2hiwbjuc24nktjjpcw3irgmbjt6ltf55uglfjjiq4u52hi6q"),
        Token(30, 10110860822564241239994147652924744222037427536707093556420917678267349073921, "bafkreiggvl7htp5n6i5e56r4nfoioy3l7j6gu6irqozzmppkismpf5j3zi"),
        Token(31, 10110860822564241239994147652924744222037427536707093556420917679366860701697, "bafkreihhkrwyibueorl7b2rz5h7dn5q6ypj6fsxahmwrjrotianqnrbl4a"),
        Token(32, 10110860822564241239994147652924744222037427536707093556420917680466372329473, "bafkreidofiu2zlubzcq4eqcm633ra3r234tcv3mtew63g7qax6v55d3hiu"),
        Token(33, 10110860822564241239994147652924744222037427536707093556420917681565883957249, "bafkreihusrizsve5lcwhpkwgbjyoif6zamdqzicns2g2xvg2wdss6qu45u"),
        Token(34, 10110860822564241239994147652924744222037427536707093556420917682665395585025, "bafkreid5y5zlye4s6rktck75b7dja2kchudy5cqkwzy7ah73pfn3qzcqmm"),
        Token(35, 10110860822564241239994147652924744222037427536707093556420917683764907212801, "bafkreicvbwcmmuvua2oud56jtposk5l672tlcnu6t7up53atgddthy7c7a"),
        Token(36, 10110860822564241239994147652924744222037427536707093556420917684864418840577, "bafkreic3mqf4ncvvl5jq5uxhdhec4ooqbholznkku22td2ucl2f2v77bju"),
        Token(37, 10110860822564241239994147652924744222037427536707093556420917685963930468353, "bafkreibp25o3lvwf3dthtcxrpdheeryq5xztjei6agzotd5hwcw6sn6xta"),
        Token(38, 10110860822564241239994147652924744222037427536707093556420917687063442096129, "bafkreigtfuouruiuv4cd62vddfq25zk4lm4kpjhba5mjd7xq2yahwymrgi"),
        Token(39, 10110860822564241239994147652924744222037427536707093556420917688162953723905, "bafkreicqyog7cwcd3coea7uurig755zjrxjycmmphexnbgsfbi7x75g5ve"),
        Token(40, 10110860822564241239994147652924744222037427536707093556420917689262465351681, "bafkreia3mk6qdc6g57qpdv7i6gnrbw7le6asgtd7k2oojdzto2upxwggvy"),
        Token(41, 10110860822564241239994147652924744222037427536707093556420917690361976979457, "bafkreihn3ihcgel4c5wdefj7xqeygoopramzhotbjnyqurek2alpq7naoa"),
        Token(42, 10110860822564241239994147652924744222037427536707093556420917691461488607233, "bafkreifahqq4k62hsmfj7w6tpy2youqeihesguwffllhpfznx57me5ulfq"),
        Token(43, 10110860822564241239994147652924744222037427536707093556420917692561000235009, "bafkreifr3yrqupqtjbavtxoixubgdgagzb6n5ynlzsdis72xo7eh5iquba"),
        Token(44, 10110860822564241239994147652924744222037427536707093556420917693660511862785, "bafkreihplkfnk4u67kxmvvphek5aaxhhgracwcfe7t6kibvwjft3unkiaq"),
        Token(45, 10110860822564241239994147652924744222037427536707093556420917694760023490561, "bafkreiate6xpg4xlopwebsffi5bbosf5os3z3d5oduo6aqpmuq7pdia72i"),
        Token(46, 10110860822564241239994147652924744222037427536707093556420917695859535118337, "bafkreigzexujx26t25v4kzl5dkpu7cfayiu5bqplazpgpfoamwr337nc5q"),
        Token(47, 10110860822564241239994147652924744222037427536707093556420917696959046746113, "bafkreibb3ezkecapwkomlnxri7teg6qatwgutcxgm4gof73nwzh2gcvzt4"),
        Token(48, 10110860822564241239994147652924744222037427536707093556420917698058558373889, "bafkreif6pir6dt67kwk2fj6gxip7gkfqtfnv2z7dayq7xtniius3bhhwfu"),
        Token(49, 10110860822564241239994147652924744222037427536707093556420917699158070001665, "bafkreib2s3ve6zo3qysnyahwsoqc2yzjf5tiuveisol33su7y6pbyiupnm"),
        Token(50, 10110860822564241239994147652924744222037427536707093556420917700257581629441, "bafkreifndagm6trbowieob6usqdaqfop7u3g4q4b6cxbqppk6bggq55aja")
    ]
)

mumbai = Environment(
    old_token = "0x2953399124f0cbb46d2cbacd8a89cf0599974963",
    opensea_proxy = "0xff7Ca10aF37178BdD056628eF42fD7F799fAc77c",
    tokens = [
        Token(1, 110058511683499541956638115260030752419186088947549686925221671937348632313857, polygon.tokens[0].uri),
        Token(2, 110058511683499541956638115260030752419186088947549686925221671938448143941633, polygon.tokens[1].uri),
        Token(3, 110058511683499541956638115260030752419186088947549686925221671939547655569409, polygon.tokens[2].uri),
        Token(4, 110058511683499541956638115260030752419186088947549686925221671940647167197185, polygon.tokens[3].uri),
        Token(5, 110058511683499541956638115260030752419186088947549686925221671941746678824961, polygon.tokens[4].uri),
        Token(6, 110058511683499541956638115260030752419186088947549686925221671942846190452737, polygon.tokens[5].uri),
        Token(7, 110058511683499541956638115260030752419186088947549686925221671943945702080513, polygon.tokens[6].uri),
        Token(8, 110058511683499541956638115260030752419186088947549686925221671945045213708289, polygon.tokens[7].uri),
        Token(9, 110058511683499541956638115260030752419186088947549686925221671946144725336065, polygon.tokens[8].uri),
        Token(10, 110058511683499541956638115260030752419186088947549686925221671947244236963841, polygon.tokens[9].uri)
    ]
)

local = Environment(
    old_token = None,
    opensea_proxy = polygon.opensea_proxy,
    tokens = polygon.tokens
)
