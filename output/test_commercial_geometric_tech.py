import bpy
import math
import random
from mathutils import Vector, Color, Euler

# Clear scene completely
bpy.ops.wm.read_homefile(use_empty=True)
while bpy.data.objects:
    bpy.data.objects.remove(bpy.data.objects[0], do_unlink=True)

# Clear all materials and textures for clean start
for mat in bpy.data.materials:
    bpy.data.materials.remove(mat)
for tex in bpy.data.textures:
    bpy.data.textures.remove(tex)

# Constants
FPS = 30
TOTAL_FRAMES = 300
DURATION = 10.0

print("=" * 80)
print("🎬 COMMERCIAL-GRADE AUDIO-REACTIVE ANIMATION SYSTEM v4.0")
print("=" * 80)
print(f"📊 Duration: {DURATION:.2f}s | Frames: {TOTAL_FRAMES} | FPS: {FPS}")
print(f"🎨 Style: geometric_tech")
print(f"🎯 Quality: COMMERCIAL BROADCAST")
print(f"⚡ Features: DRAMATIC VISUALS | HIGH CONTRAST | COMMERCIAL LIGHTING")
print("=" * 80)

# Enhanced audio data with better compression
AUDIO_DATA = {"duration": 10.0, "fps": 30, "total_frames": 300, "bass": [0.25533129736976184, 0.34059033626741064, 0.4784936533606947, 0.5287599142784213, 0.435295061649115, 0.5747185234280491, 0.5676924604946321, 0.6864693966061994, 0.6101362394740493, 0.7118214480276863, 0.6518538786255261, 0.7725655815239358, 0.7376927664329752, 0.7621522411361376, 0.8041745689671645, 0.8785529454158555, 0.918379329472874, 0.8590148707246317, 0.8276781896908312, 0.7665355926938952, 0.8448856711831888, 0.714811241219387, 0.7607025565546957, 0.7037567195992344, 0.5778228096284747, 0.7313290557320293, 0.6492454126084276, 0.5967269798836862, 0.5900791553596538, 0.5808277385790027, 0.5031386450698735, 0.42186690659544185, 0.5408052528580574, 0.5005542615882362, 0.35344175631331476, 0.3132931327781191, 0.4656177194981232, 0.46877068423137697, 0.3814702257787087, 0.38318946914797747, 0.39979362341435043, 0.4895028373765681, 0.3872164158348711, 0.45658195445913863, 0.43743583420096566, 0.5215618486953935, 0.5862334287311376, 0.5357029400675698, 0.6395687662049024, 0.6079772650804196, 0.598689161906523, 0.7277066835426445, 0.7768412178672482, 0.7441146045004583, 0.7330024994537799, 0.7213649519311642, 0.7662487176812722, 0.7084993085585396, 0.8055235960059876, 0.9043244423968586, 0.8522452168206602, 0.8027391638307196, 0.7209099656629262, 0.8533802364780607, 0.8531382943467116, 0.7430710196709855, 0.7395452249883113, 0.7017071727333215, 0.5788536846180775, 0.5676358625565546, 0.6159991403928989, 0.49774755492612943, 0.5451812158143613, 0.39126079880278136, 0.45055215696587264, 0.24226921398710732, 0.3409295762334948, 0.1435574997046636, 0.07356745858789468, 0.07921782639402702, 0.024402236117632592, 0.0098647287120016, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.014885983357964858, 0.020378255963133862, 0.12245744930875777, 0.09586147846514659, 0.06267571002311204, 0.20707274038184484, 0.19568267316932764, 0.13652444301915917, 0.17400033003713317, 0.20990668946103463, 0.12946430190948605, 0.2415921605358642, 0.12293367366150776, 0.193362112116533, 0.15914891773426237, 0.06256154358117932, 0.17300542778896053, 0.17862054011247233, 0.14791227114143793, 0.150447903536903, 0.0, 0.0, 0.03943268384073375, 0.036138558649863636, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.08303107113260313, 0.0, 0.11233957135347981, 0.06504795719774109, 0.2226928474499826, 0.3037521363035409, 0.3324446956029622, 0.2665812873302509, 0.31492896695320205, 0.3649384611747619, 0.4634744003115102, 0.5964274717298133, 0.5343904676128222, 0.6697176282954859, 0.698039903267775, 0.8020834070052478, 0.7252211682573778, 0.6810075466959661, 0.714347231396228, 0.8514778738603885, 0.85216227692343, 0.7570059081120725, 0.7382715831062625, 0.746562633925661, 0.8235244576673459, 0.721725567120731, 0.8407102304377662, 0.8122100939011778, 0.7078338565717276, 0.7450942090083632, 0.7172288855513441, 0.7170826996382795, 0.5736054574177596, 0.5068511006446175, 0.6229098999311268, 0.6190552016765052, 0.4731035736183885, 0.4700148345972649, 0.472543735677295, 0.43943169846068875, 0.48377945949926404, 0.3594896766835604, 0.3745963591433715, 0.3536892034940524, 0.35306774264229535, 0.4817678101081002, 0.44002778062298253, 0.42809476369249033, 0.36459092579606733, 0.5148299599306437, 0.43735305410240843, 0.47494212138780884, 0.4432128254479166, 0.5492975290884742, 0.6815248261276491, 0.6675411856930455, 0.5657396782730558, 0.6560529911403528, 0.6467535341519468, 0.8170899450229694, 0.7614017584855263, 0.6822628215948723, 0.7892939080881713, 0.8341925315640097, 0.7263291735070351, 0.8411888165703112, 0.8458950840927063, 0.7802233115749927, 0.88418637344408, 0.7324042620109888, 0.6773001595327458, 0.7251064752708389, 0.7172733271244408, 0.6248361709125603, 0.7129368441800109, 0.5734463957153951, 0.47682734025271933, 0.5634010632665298, 0.4163189566563734, 0.3869282152608935, 0.43105449033949883, 0.2663263321327225, 0.24545209356496092, 0.2769759512845539, 0.22397974210981791, 0.05938283524073719, 0.0, 0.0, 0.00085147172567962, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.03173146224916226, 0.0, 0.0812402137845253, 0.008258861142014316, 0.15172141100650924, 0.21537533758014032, 0.1187664501903268, 0.19509373319881465, 0.25252543215723744, 0.2802669994665863, 0.25822381446738185, 0.23965891648448945, 0.18749279728340235, 0.15430896529031773, 0.1860189157250652, 0.09353557755582938, 0.10819654791936781, 0.18217293075716023, 0.05556829291158619, 0.05701344351744719, 0.10371004203602999, 0.0, 0.04591464386053752, 0.0037433712428606297, 0.0, 0.014898857842678526, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.04789534780233758, 0.19993314608886378, 0.1434043812116707, 0.2776691710841057], "mid": [0.20770971463293889, 0.25132789916664694, 0.35679138505928915, 0.3860098950870032, 0.36519011710255944, 0.48689372024767075, 0.5051346343403896, 0.5332209709785665, 0.5826525926921908, 0.514026990423994, 0.5364800133015339, 0.539379870615558, 0.586778095833938, 0.5001326559136563, 0.574446373158725, 0.5080848005398866, 0.5169023349372053, 0.40714315056902806, 0.43994548874730144, 0.40347152496275956, 0.39284748062340596, 0.3941532907795714, 0.3223365935105391, 0.28887551023237656, 0.31349402231099904, 0.33720960060143157, 0.3365716568209889, 0.31173031453416333, 0.35260970421416094, 0.3417631525579579, 0.3571141943951577, 0.38405427047869733, 0.4481166024707046, 0.45042530066139524, 0.4563525255197369, 0.519572162955306, 0.4878297927872527, 0.5152640564124268, 0.5647311383278204, 0.5513174640200409, 0.5498352967285062, 0.513146441296513, 0.4968466516186353, 0.5379953233493895, 0.454811124963665, 0.4930052558338223, 0.4363589707037261, 0.3768702167651734, 0.294821897016472, 0.2418860314220002, 0.23570878246581806, 0.14051650556296266, 0.057485137489466036, 0.0756375026445183, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0030068272536353594, 0.0, 0.07092191996732736, 0.018291420504044295, 0.1105298561450608, 0.06975639602758738, 0.08894797617509784, 0.07857422199379535, 0.0702076187681708, 0.11876463618073825, 0.1161880960994117, 0.10459228773575999, 0.07402861614410731, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.011150225138143347, 0.11233693385783644, 0.15655821199785164, 0.21179883227657972, 0.30094259253155053, 0.2879155039243967, 0.40311354061214144, 0.37974324136142185, 0.4435004495117256, 0.5068601502611837, 0.5256432257165412, 0.5028211270741911, 0.53412009533369, 0.5247385345417891, 0.5982339119177317, 0.5449602093656757, 0.5823333796966351, 0.48186322122778336, 0.5166889842702026, 0.5137508008245008, 0.4825466284417785, 0.4145878161253638, 0.35174834752740675, 0.33312621610641324, 0.36938445214903237, 0.323918632303093, 0.34179970579832386, 0.2926933623188686, 0.25356992963633274, 0.28527653802997927, 0.33854890361788925, 0.31719393087764297, 0.31953448613343494, 0.33249172011190475, 0.34877568728360236, 0.3898328610862166, 0.40862593574575123, 0.5098317078811486, 0.5451857000759874, 0.541581142320144, 0.5796998384971714, 0.6001765898444377, 0.5657940069614882, 0.6033396845985638, 0.5655531670334363, 0.5937307499090922, 0.5287292801285076, 0.5045461665922343, 0.44870381338550863, 0.3882915784345858, 0.3438342375188399, 0.35279986261175444, 0.27097190671179905, 0.20333781283846064, 0.15471577880443235, 0.0711188056802151, 0.056110168562525584, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.023955928258397458, 0.01474942332401697, 0.07789070486673084, 0.10642045880007105, 0.045740936395195636, 0.12216600009100975, 0.08619677027162648, 0.0789305947554694, 0.11015586420539507, 0.04671706605772581, 0.050327086165823785, 0.013836681031747296, 0.025749978630259823, 0.0002709121473460224, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.008204511541083204, 0.07972971962875507, 0.09075480748438097, 0.11857816587539476, 0.15806367216420866, 0.28509295867371487, 0.2859766007975883, 0.397745454755744, 0.4463520784362627, 0.4728783294242259, 0.4802058382538413, 0.4825517188585557, 0.52392828875649, 0.5793411113329344, 0.558871133945425, 0.5627348628867822, 0.5940013866180217, 0.5918464268510056, 0.5241877557471715, 0.4698640812539586, 0.5214486382649939, 0.4501375835804307, 0.42593829423288404, 0.405920395896359, 0.3599197040134154, 0.3318750263965699, 0.3750248432252852, 0.3434164926289763, 0.311868295912352, 0.25542294849113717, 0.3501737254126257, 0.2967634618673915, 0.2786762708450845, 0.39393435710503977, 0.38370375848312754, 0.3879156704212875, 0.46556940873904856, 0.4252791140849093, 0.5215022686680901, 0.4740139751537554, 0.5098850325205522, 0.5111923967456077, 0.5998558033890126, 0.6120534274173843, 0.5542501682897938, 0.5469539166551989, 0.5574412656759062, 0.4789034691827944, 0.5274756416609144, 0.4810574499584988, 0.39750879604009887, 0.3240155922733949, 0.2794042177284048, 0.25793373853701085, 0.17556714873389712, 0.14308847979535902, 0.12452819472579679, 0.04529112733838127, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.04078773933956713, 0.018317730852682422, 0.07683716717829667, 0.11972818448367888, 0.11245139867202919, 0.05974208258858167, 0.09376386389680767, 0.06791891142759407, 0.12489922337713556, 0.056912897734207116, 0.05015399986698256, 0.023330735158790014, 0.01241697130739109, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.06893051751997985, 0.12004795144258781, 0.1299100829349027], "high": [0.07170138035752113, 0.1683245310302547, 0.17424889572564387, 0.21568564839869075, 0.27270976773694666, 0.28675266803911387, 0.2969460194095919, 0.3206599502551372, 0.3157302205369595, 0.3326206029508023, 0.2937483810104965, 0.3211077004071966, 0.25424040214628557, 0.24227783627433136, 0.2307982066784884, 0.2421483596547817, 0.2057066312463846, 0.22215144009980475, 0.22772383270799748, 0.18653723597836536, 0.19711297579189782, 0.2020331249696385, 0.24921759181785758, 0.24925045062241352, 0.24209715014804553, 0.28317790338769266, 0.2706692575670068, 0.32614958917927467, 0.34074771109097773, 0.3247794089912049, 0.31696981892136245, 0.32987358316034865, 0.2668053462778078, 0.2670710260005901, 0.24687692616042367, 0.22480216049408525, 0.13297882894053314, 0.10125575759954841, 0.08198477136938118, 0.011636645537791663, 0.003621921588062932, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.011447097243951293, 0.0012200759179431392, 0.025361582431003983, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.008803659759931103, 0.06887447449357423, 0.11513794204822511, 0.11562967912785224, 0.17963402356346164, 0.18919720391583825, 0.23716440301703526, 0.28652781654009607, 0.2780419467589214, 0.2982139098175287, 0.28960994425260217, 0.3166512127057493, 0.3323478684185251, 0.2952050661790188, 0.2971155525152393, 0.27906068724590594, 0.22703102362504926, 0.252833205387047, 0.22822880101228657, 0.19636747928805487, 0.18254432375212049, 0.17062800907785503, 0.22234414604981803, 0.18616207583291844, 0.249061222701849, 0.22384237213144884, 0.2836497659163937, 0.27650835117833333, 0.3008836470222392, 0.27275228655413575, 0.3005636793078531, 0.3015672319281398, 0.3364868892302275, 0.3199741317934209, 0.28714700761804113, 0.2530958581055507, 0.20626810723642935, 0.228649055629512, 0.1709178852445732, 0.12056849850264492, 0.06524959638757909, 0.04997927510564163, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.002499197121602084, 0.003923897711316092, 0.0, 0.014124744939584183, 0.02267460507331942, 0.013702755495995707, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0104172446718525, 0.07927520655127719, 0.11059995348801475, 0.15855647863600403, 0.20484673243075138, 0.21429449266417283, 0.2723254688052926, 0.2978280340076216, 0.27242176223399867, 0.3108999195930068, 0.32245336270194186, 0.29023565280452335, 0.28264036260415737, 0.3208367471952248, 0.2572286160895684, 0.266406344607903, 0.26304441616051955, 0.2513802045110409, 0.23500014765403243, 0.2300544301565724, 0.18464795113527374, 0.21491687910428958, 0.22661578825059914, 0.2194831819771748, 0.2402221663814577, 0.21549464332099755, 0.23580547000633426, 0.2753785467093118, 0.2757129483485167, 0.3271670335785296, 0.29849250272265326, 0.32037366666691824, 0.3413258459369514, 0.3144682962412557, 0.300647893314765, 0.2348856201505588, 0.23610535931574522, 0.1906515959976134, 0.18536581098843694, 0.1033061263175656, 0.07026217677113192, 0.05834378901745695, 0.026012870231806012, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.004743633348392368, 0.023782170820131412, 0.005650970615214246, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.01118040673723112, 0.008652241677960956, 0.046718374198790075, 0.11113691716964708, 0.12218059462020395, 0.18155134373903695, 0.2161036784240546, 0.23914321859520715, 0.2633134552167126, 0.29988119890826087, 0.2903936755479056, 0.3008710998293241, 0.2960948271078378, 0.3083830087275038, 0.27476370460121713, 0.28244754995102295, 0.25522736821750325, 0.27246343613569124, 0.24513674299102856, 0.18993166896661742, 0.23142857510153655, 0.21902029224195466, 0.2169242298258413, 0.2066542442598545, 0.21547306642843045, 0.20950879947437318, 0.2484559422392616, 0.22793183590672694, 0.2750838890145057, 0.2830479007891761, 0.3270853771445153, 0.28792205983398655, 0.30650338731893295, 0.29160464127121194, 0.3283952974430564, 0.28632825254381866, 0.2912656007217786, 0.25621992808572597, 0.20814632100880465, 0.1811773581157367, 0.10496164932707104, 0.08707987326657243, 0.02678920163328279, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0034297124898068146, 0.023469272640368855, 0.020700554070574688, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.011838352433175433, 0.07686112767395929]}
_audio_cache = {}

def get_audio(channel, frame, smooth=15):
    """Enhanced audio data retrieval with better smoothing."""
    key = (channel, frame, smooth)
    if key in _audio_cache:
        return _audio_cache[key]
    
    data = AUDIO_DATA.get(channel, [])
    if not data:
        return 0.5
    
    # Better frame-to-data mapping
    frame_ratio = frame / TOTAL_FRAMES
    idx = min(int(frame_ratio * len(data)), len(data) - 1)
    
    # Enhanced smoothing with adaptive window
    window = max(1, smooth // 2)
    start = max(0, idx - window)
    end = min(len(data), idx + window + 1)
    values = data[start:end]
    
    # Add some variation for more dynamic response
    base_value = sum(values) / len(values) if values else 0.5
    variation = random.uniform(0.95, 1.05)  # Small random variation
    result = min(1.0, max(0.0, base_value * variation))
    
    _audio_cache[key] = result
    return result

def add_bezier_keyframe(obj, data_path, frame):
    """Enhanced keyframe insertion with smooth interpolation."""
    obj.keyframe_insert(data_path=data_path, frame=frame)
    if obj.animation_data and obj.animation_data.action:
        for fcurve in obj.animation_data.action.fcurves:
            if data_path in fcurve.data_path:
                for kp in fcurve.keyframe_points:
                    if abs(kp.co[0] - frame) < 0.1:
                        kp.interpolation = 'BEZIER'
                        kp.handle_left_type = 'AUTO_CLAMPED'
                        kp.handle_right_type = 'AUTO_CLAMPED'
                        # Ensure smooth curves
                        kp.handle_left = (kp.co[0] - 0.1, kp.co[1])
                        kp.handle_right = (kp.co[0] + 0.1, kp.co[1])

# COMMERCIAL-GRADE material creation system
_material_cache = {}

def create_commercial_material(name, color, metallic=0.0, roughness=0.5, emission_strength=0.0, 
                              fresnel=True, anisotropic=0.0, sheen=0.0, clearcoat=0.0, 
                              subsurface=0.0, transmission=0.0):
    """Create commercial-grade PBR material with dramatic visual impact."""
    if name in _material_cache:
        return _material_cache[name]
    
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (800, 0)
    
    # Principled BSDF with all advanced features
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (400, 0)
    bsdf.inputs['Base Color'].default_value = color
    bsdf.inputs['Metallic'].default_value = metallic
    bsdf.inputs['Roughness'].default_value = roughness
    bsdf.inputs['Specular IOR Level'].default_value = 0.5
    
    # Advanced material properties for commercial quality
    bsdf.inputs['Anisotropic'].default_value = anisotropic
    bsdf.inputs['Sheen Weight'].default_value = sheen
    bsdf.inputs['Coat Weight'].default_value = clearcoat
    bsdf.inputs['Coat Roughness'].default_value = roughness * 0.3
    bsdf.inputs['Subsurface Weight'].default_value = subsurface
    bsdf.inputs['Subsurface Radius'].default_value = (1.0, 0.2, 0.1)
    bsdf.inputs['Transmission Weight'].default_value = transmission
    
    # DRAMATIC emission setup for high visibility
    if emission_strength > 0:
        mix_shader = nodes.new('ShaderNodeMixShader')
        mix_shader.location = (600, 0)
        
        emission_node = nodes.new('ShaderNodeEmission')
        emission_node.location = (200, 200)
        emission_node.inputs['Color'].default_value = color
        emission_node.inputs['Strength'].default_value = emission_strength
        
        # Fresnel for realistic edge glow
        if fresnel:
            fresnel_node = nodes.new('ShaderNodeFresnel')
            fresnel_node.location = (0, 100)
            fresnel_node.inputs['IOR'].default_value = 1.45
            
            colorramp = nodes.new('ShaderNodeValToRGB')
            colorramp.location = (200, 100)
            colorramp.color_ramp.elements[0].position = 0.3
            colorramp.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
            colorramp.color_ramp.elements[1].position = 0.9
            colorramp.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
            
            links.new(fresnel_node.outputs['Fac'], colorramp.inputs['Fac'])
            links.new(colorramp.outputs['Color'], mix_shader.inputs['Fac'])
        else:
            mix_shader.inputs['Fac'].default_value = 0.8
        
        links.new(emission_node.outputs['Emission'], mix_shader.inputs[1])
        links.new(bsdf.outputs['BSDF'], mix_shader.inputs[2])
        links.new(mix_shader.outputs['Shader'], output.inputs['Surface'])
    else:
        links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    
    # Performance optimizations
    mat.use_backface_culling = True
    
    _material_cache[name] = mat
    return mat

# COMMERCIAL-GRADE SCENE CONFIGURATION
print("🔧 Setting up commercial-grade scene...")

scene = bpy.context.scene
scene.frame_start = 1
scene.frame_end = TOTAL_FRAMES
scene.render.fps = FPS
scene.render.resolution_x = 1280
scene.render.resolution_y = 720
scene.render.resolution_percentage = 100

# COMMERCIAL RENDER ENGINE: Cycles for maximum quality
scene.render.engine = 'CYCLES'
scene.cycles.samples = 64
scene.cycles.use_denoising = True
scene.cycles.denoiser = 'OPENIMAGEDENOISE'
scene.cycles.denoising_input_passes = 'RGB_ALBEDO_NORMAL'
scene.cycles.device = 'GPU'
scene.cycles.use_adaptive_sampling = True
scene.cycles.adaptive_threshold = 0.01

# COMMERCIAL LIGHT PATHS for realistic rendering
scene.cycles.max_bounces = 16
scene.cycles.diffuse_bounces = 6
scene.cycles.glossy_bounces = 6
scene.cycles.transmission_bounces = 16
scene.cycles.volume_bounces = 2
scene.cycles.transparent_max_bounces = 12

# Caustics for dramatic reflections
scene.cycles.caustics_reflective = True
scene.cycles.caustics_refractive = True
scene.cycles.blur_glossy = 0.3

# Motion blur for commercial look
scene.render.use_motion_blur = True
scene.render.motion_blur_shutter = 0.5

# Video output settings
scene.render.image_settings.file_format = 'FFMPEG'
scene.render.ffmpeg.format = 'MPEG4'
scene.render.ffmpeg.codec = 'H264'
scene.render.ffmpeg.constant_rate_factor = 'HIGH'
scene.render.ffmpeg.ffmpeg_preset = 'BEST'

# COMMERCIAL COLOR MANAGEMENT
scene.view_settings.view_transform = 'AgX'
scene.view_settings.look = 'AgX - Very High Contrast'
scene.sequencer_colorspace_settings.name = 'Linear Rec.709'

# DRAMATICALLY IMPROVED CAMERA SETUP
camera_data = bpy.data.cameras.new('Camera')
camera_data.lens = 35  # Wide angle for dramatic framing
camera_data.dof.use_dof = True
camera_data.dof.aperture_fstop = 2.8
camera_data.dof.focus_distance = 8  # Closer focus for dramatic effect

camera_obj = bpy.data.objects.new('Camera', camera_data)
scene.collection.objects.link(camera_obj)

# FIXED: Proper camera positioning for maximum visibility
camera_obj.location = (0, -8, 4)  # Closer and better positioned
camera_obj.rotation_euler = (math.radians(70), 0, 0)  # Better viewing angle
scene.camera = camera_obj

# COMMERCIAL-GRADE LIGHTING SYSTEM
def create_commercial_light(name, location, rotation, power, size, color, shadow=True):
    """Create professional lighting with dramatic intensity."""
    light_data = bpy.data.lights.new(name, 'AREA')
    light_data.energy = power  # High intensity for commercial look
    light_data.size = size
    light_data.color = color
    light_data.use_shadow = shadow
    if shadow:
        light_data.shadow_soft_size = 2.0
    
    light_obj = bpy.data.objects.new(name, light_data)
    scene.collection.objects.link(light_obj)
    light_obj.location = location
    light_obj.rotation_euler = rotation
    return light_obj

# DRAMATIC 4-POINT LIGHTING SYSTEM
# Key Light - Main dramatic illumination
key_light = create_commercial_light(
    'KeyLight', 
    (8, -8, 12), 
    (math.radians(45), 0, math.radians(45)), 
    25000,  # Very high intensity
    12, 
    (1.0, 0.95, 0.85)
)

# Fill Light - Soften shadows
fill_light = create_commercial_light(
    'FillLight', 
    (-6, -6, 8), 
    (math.radians(30), 0, math.radians(-30)), 
    15000, 
    18, 
    (0.6, 0.7, 1.0)
)

# Rim Light - Edge definition
rim_light = create_commercial_light(
    'RimLight', 
    (0, 10, 10), 
    (math.radians(-45), 0, 0), 
    20000, 
    10, 
    (1.0, 0.8, 0.5)
)

# Accent Light - Additional drama
accent_light = create_commercial_light(
    'AccentLight', 
    (6, 6, 12), 
    (math.radians(-60), 0, math.radians(30)), 
    12000, 
    8, 
    (0.8, 0.9, 1.0)
)

# DRAMATIC WORLD SETUP
world = bpy.data.worlds.new("CommercialWorld")
scene.world = world
world.use_nodes = True
nodes = world.node_tree.nodes
links = world.node_tree.links
nodes.clear()

output = nodes.new('ShaderNodeOutputWorld')
output.location = (600, 0)

# Background with dramatic gradient
bg = nodes.new('ShaderNodeBackground')
bg.location = (400, 0)

# Create dramatic gradient
coord = nodes.new('ShaderNodeTexCoord')
coord.location = (0, 0)
mapping = nodes.new('ShaderNodeMapping')
mapping.location = (200, 0)
grad = nodes.new('ShaderNodeTexGradient')
grad.location = (400, 0)
colorramp = nodes.new('ShaderNodeValToRGB')
colorramp.location = (600, 0)

# Dramatic color gradient
colorramp.color_ramp.elements[0].position = 0.0
colorramp.color_ramp.elements[0].color = (0.01, 0.01, 0.02, 1.0)  # Very dark
colorramp.color_ramp.elements[1].position = 1.0
colorramp.color_ramp.elements[1].color = (0.05, 0.05, 0.1, 1.0)  # Slightly lighter

bg.inputs['Strength'].default_value = 2.0  # High intensity

# Connect nodes
links.new(coord.outputs['Generated'], mapping.inputs['Vector'])
links.new(mapping.outputs['Vector'], grad.inputs['Vector'])
links.new(grad.outputs['Color'], colorramp.inputs['Fac'])
links.new(colorramp.outputs['Color'], bg.inputs['Color'])
links.new(bg.outputs[0], output.inputs[0])

print("✅ Commercial-grade scene setup complete")
print(f"   Camera: {'✅' if scene.camera else '❌'} positioned at {camera_obj.location}")
print(f"   Lights: {len([obj for obj in scene.objects if obj.type == 'LIGHT'])} commercial lights")
print(f"   Render engine: {scene.render.engine} with {scene.cycles.samples} samples")
print(f"   Resolution: {scene.render.resolution_x}x{scene.render.resolution_y}")

# COMMERCIAL-GRADE COMPOSITOR
print("🎨 Setting up commercial compositor...")

scene.use_nodes = True
tree = scene.node_tree
nodes = tree.nodes
links = tree.links
nodes.clear()

# Input
render = nodes.new('CompositorNodeRLayers')
render.location = (0, 0)

# DRAMATIC GLARE EFFECT
glare = nodes.new('CompositorNodeGlare')
glare.location = (200, 0)
glare.glare_type = 'FOG_GLOW'
glare.quality = 'HIGH'
glare.threshold = 0.5  # Lower threshold for more dramatic effect
glare.size = 12  # Larger size for more impact

# COLOR CORRECTION for commercial look
color_correction = nodes.new('CompositorNodeColorCorrection')
color_correction.location = (400, 0)
color_correction.master_saturation = 1.3  # Enhanced saturation
color_correction.master_contrast = 1.2   # Higher contrast
color_correction.master_gamma = 1.1      # Slight gamma boost

# VIBRANCE for dramatic colors
vibrance = nodes.new('CompositorNodeColorCorrection')
vibrance.location = (600, 0)
vibrance.master_vibrance = 1.4  # High vibrance for impact

# FINAL OUTPUT
composite = nodes.new('CompositorNodeComposite')
composite.location = (800, 0)

# Connect the compositor chain
links.new(render.outputs[0], glare.inputs[0])
links.new(glare.outputs[0], color_correction.inputs[1])
links.new(color_correction.outputs[0], vibrance.inputs[1])
links.new(vibrance.outputs[0], composite.inputs[0])

print("✅ Commercial compositor configured with dramatic effects")

# DRAMATIC COMMERCIAL-GRADE SCENE
print("🎬 Creating dramatic commercial scene...")

# MAIN CORE SPHERE - Central focus with dramatic presence
bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=4, radius=2.0, location=(0, 0, 0))
core = bpy.context.active_object
core.name = 'CoreSphere'

# Add subdivision for smooth appearance
subdiv = core.modifiers.new('Subdiv', 'SUBSURF')
subdiv.levels = 3
subdiv.render_levels = 4

# Add displacement for audio reactivity
displace = core.modifiers.new('Displace', 'DISPLACE')
tex = bpy.data.textures.new('CoreDisplace', 'VORONOI')
tex.noise_scale = 1.5
displace.texture = tex
displace.strength = 0.0  # Will be animated

# DRAMATIC core material with high emission
core_mat = create_commercial_material(
    'CoreMat', 
    (0.2, 0.6, 1.0, 1.0), 
    metallic=0.9, 
    roughness=0.1, 
    emission_strength=50.0,  # Very high emission for visibility
    fresnel=True, 
    anisotropic=0.3, 
    clearcoat=0.2
)
core.data.materials.append(core_mat)
bpy.ops.object.shade_smooth()

# ORBITING PARTICLE SYSTEM - Multiple layers for complexity
# Layer 1: Inner particles (close to core)
for i in range(8):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=0.3, location=(0, 0, 0))
    particle = bpy.context.active_object
    particle.name = f'InnerParticle{i}'
    
    angle = (i / 8) * 2 * math.pi
    radius = 3.5
    particle.location = (math.cos(angle) * radius, math.sin(angle) * radius, 0)
    
    hue = i / 8
    particle_mat = create_commercial_material(
        f'InnerParticleMat{i}',
        (0.3 + hue * 0.7, 0.4 + (1-hue) * 0.6, 1.0, 1.0),
        metallic=0.8, 
        roughness=0.2, 
        emission_strength=40.0,  # High emission
        fresnel=True
    )
    particle.data.materials.append(particle_mat)
    bpy.ops.object.shade_smooth()

# Layer 2: Mid orbs (medium distance)
for i in range(6):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=3, radius=0.6, location=(0, 0, 0))
    orb = bpy.context.active_object
    orb.name = f'MidOrb{i}'
    
    subdiv = orb.modifiers.new('Subdiv', 'SUBSURF')
    subdiv.levels = 2
    subdiv.render_levels = 3
    
    angle = (i / 6) * 2 * math.pi + math.pi / 12
    radius = 5.5
    height = math.sin(angle * 2) * 1.0
    orb.location = (math.cos(angle) * radius, math.sin(angle) * radius, height)
    
    hue = i / 6
    orb_mat = create_commercial_material(
        f'MidOrbMat{i}',
        (0.4 + hue * 0.6, 0.5 + (1-hue) * 0.5, 0.9 - hue * 0.2, 1.0),
        metallic=0.7, 
        roughness=0.15, 
        emission_strength=35.0,  # High emission
        fresnel=True, 
        sheen=0.2
    )
    orb.data.materials.append(orb_mat)
    bpy.ops.object.shade_smooth()

# Layer 3: Outer rings (dramatic visual elements)
for i in range(3):
    bpy.ops.mesh.primitive_torus_add(
        major_radius=7.0 + i * 1.0,
        minor_radius=0.2,
        major_segments=96,
        minor_segments=32,
        location=(0, 0, 0)
    )
    ring = bpy.context.active_object
    ring.name = f'OuterRing{i}'
    
    # Varied orientations for visual interest
    if i == 0:
        ring.rotation_euler = (math.radians(90), 0, 0)
    elif i == 1:
        ring.rotation_euler = (0, math.radians(90), 0)
    else:
        ring.rotation_euler = (math.radians(45), math.radians(45), 0)
    
    ring_mat = create_commercial_material(
        f'RingMat{i}',
        (0.5 + i * 0.2, 0.4, 1.0 - i * 0.2, 1.0),
        metallic=0.95, 
        roughness=0.05, 
        emission_strength=60.0,  # Very high emission for rings
        anisotropic=0.5
    )
    ring.data.materials.append(ring_mat)
    bpy.ops.object.shade_smooth()

# AMBIENT PARTICLE SYSTEM - Atmospheric elements
for i in range(20):
    bpy.ops.mesh.primitive_ico_sphere_add(
        subdivisions=1,
        radius=random.uniform(0.08, 0.2),
        location=(0, 0, 0)
    )
    ambient = bpy.context.active_object
    ambient.name = f'AmbientParticle{i}'
    
    # Random positioning in spherical volume
    theta = random.uniform(0, 2 * math.pi)
    phi = random.uniform(0, math.pi)
    r = random.uniform(8, 12)
    
    ambient.location = (
        r * math.sin(phi) * math.cos(theta),
        r * math.sin(phi) * math.sin(theta),
        r * math.cos(phi)
    )
    
    ambient_mat = create_commercial_material(
        f'AmbientMat{i}',
        (random.uniform(0.7, 1.0), random.uniform(0.7, 0.9), 1.0, 1.0),
        metallic=0.6, 
        roughness=0.3, 
        emission_strength=random.uniform(20, 40)
    )
    ambient.data.materials.append(ambient_mat)
    bpy.ops.object.shade_smooth()

print("✅ Dramatic commercial scene created")
print(f"   Total objects: {{len(bpy.data.objects)}}")
print(f"   Core sphere: {{'✅' if bpy.data.objects.get('CoreSphere') else '❌'}}")
print(f"   Inner particles: {{len([obj for obj in bpy.data.objects if obj.name.startswith('InnerParticle')])}}")
print(f"   Mid orbs: {{len([obj for obj in bpy.data.objects if obj.name.startswith('MidOrb')])}}")
print(f"   Outer rings: {{len([obj for obj in bpy.data.objects if obj.name.startswith('OuterRing')])}}")
print(f"   Ambient particles: {{len([obj for obj in bpy.data.objects if obj.name.startswith('AmbientParticle')])}}")

# HIGHLY REACTIVE DRAMATIC ANIMATION SYSTEM
print("🎬 Creating highly reactive animations...")

# DRAMATIC CAMERA ANIMATION - Cinematic movement
camera = scene.camera
for frame in range(1, TOTAL_FRAMES + 1, 1):  # Every frame for smoothness
    t = frame / TOTAL_FRAMES
    bass = get_audio('bass', frame, 10)
    mid = get_audio('mid', frame, 8)
    high = get_audio('high', frame, 6)
    
    # DRAMATIC camera movement with better framing
    angle = t * math.pi * 1.5  # Slower, more cinematic
    radius = 6 + bass * 1.5 + mid * 1.0  # Closer for better visibility
    height = 3 + mid * 1.0 + high * 0.8 + math.sin(t * math.pi * 2) * 1.0
    
    camera.location = (
        math.sin(angle) * radius, 
        -math.cos(angle) * radius, 
        height
    )
    add_bezier_keyframe(camera, 'location', frame)
    
    # Camera rotation for dynamic framing
    camera.rotation_euler.x = math.radians(70) + mid * 0.1
    camera.rotation_euler.z = angle + math.pi / 2
    add_bezier_keyframe(camera, 'rotation_euler', frame)

# CORE SPHERE - Highly reactive to bass
core = bpy.data.objects.get('CoreSphere')
if core:
    for frame in range(1, TOTAL_FRAMES + 1, 1):
        t = frame / TOTAL_FRAMES
        bass = get_audio('bass', frame, 8)
        mid = get_audio('mid', frame, 6)
        high = get_audio('high', frame, 4)
        
        # DRAMATIC scaling based on audio
        energy = (bass * 0.6 + mid * 0.3 + high * 0.1)
        scale = 1.0 + energy * 1.2  # More dramatic scaling
        core.scale = (scale, scale, scale)
        add_bezier_keyframe(core, 'scale', frame)
        
        # Displacement animation
        if core.modifiers.get('Displace'):
            core.modifiers['Displace'].strength = bass * 0.5 + mid * 0.3
        
        # Rotation
        core.rotation_euler = (
            t * math.pi * 1.8, 
            t * math.pi * 2.2, 
            t * math.pi * 2.8
        )
        add_bezier_keyframe(core, 'rotation_euler', frame)

# INNER PARTICLES - Responsive to high frequencies
inner_particles = [obj for obj in bpy.data.objects if obj.name.startswith('InnerParticle')]
for i, particle in enumerate(inner_particles):
    phase = (i / len(inner_particles)) * 2 * math.pi
    for frame in range(1, TOTAL_FRAMES + 1, 1):
        t = frame / TOTAL_FRAMES
        bass = get_audio('bass', frame, 8)
        mid = get_audio('mid', frame, 6)
        high = get_audio('high', frame, 4)
        
        # Orbital movement
        angle = t * math.pi * 2.5 + phase
        radius = 3.5 + bass * 1.5 + mid * 1.0
        height = math.sin(t * math.pi * 3 + phase) * 0.8 + high * 1.0
        
        particle.location = (
            math.cos(angle) * radius, 
            math.sin(angle) * radius, 
            height
        )
        add_bezier_keyframe(particle, 'location', frame)
        
        # Scaling
        scale = 1.0 + bass * 0.6 + mid * 0.4 + high * 0.3
        particle.scale = (scale, scale, scale)
        add_bezier_keyframe(particle, 'scale', frame)
        
        # Rotation
        particle.rotation_euler = (
            t * math.pi * 3 + phase, 
            t * math.pi * 2.5 + phase, 
            t * math.pi * 4 + phase
        )
        add_bezier_keyframe(particle, 'rotation_euler', frame)

# MID ORBS - Balanced reactivity
mid_orbs = [obj for obj in bpy.data.objects if obj.name.startswith('MidOrb')]
for i, orb in enumerate(mid_orbs):
    phase = (i / len(mid_orbs)) * 2 * math.pi
    for frame in range(1, TOTAL_FRAMES + 1, 1):
        t = frame / TOTAL_FRAMES
        bass = get_audio('bass', frame, 8)
        mid = get_audio('mid', frame, 6)
        high = get_audio('high', frame, 4)
        
        # Orbital movement
        angle = t * math.pi * 2.0 + phase
        radius = 5.5 + mid * 1.2 + bass * 0.8
        height = math.sin(angle * 1.5 + t * math.pi * 4) * 1.2 + high * 0.8
        
        orb.location = (
            math.cos(angle) * radius,
            math.sin(angle) * radius,
            height
        )
        add_bezier_keyframe(orb, 'location', frame)
        
        # Scaling
        scale = 1.0 + (bass * 0.5 + mid * 0.5 + high * 0.3)
        orb.scale = (scale, scale, scale)
        add_bezier_keyframe(orb, 'scale', frame)
        
        # Rotation
        orb.rotation_euler = (
            t * math.pi * 2.2 + phase,
            t * math.pi * 1.8 + phase,
            t * math.pi * 2.6 + phase
        )
        add_bezier_keyframe(orb, 'rotation_euler', frame)

# OUTER RINGS - Dramatic rotation
rings = [obj for obj in bpy.data.objects if obj.name.startswith('OuterRing')]
for i, ring in enumerate(rings):
    for frame in range(1, TOTAL_FRAMES + 1, 1):
        t = frame / TOTAL_FRAMES
        bass = get_audio('bass', frame, 10)
        mid = get_audio('mid', frame, 8)
        high = get_audio('high', frame, 6)
        
        # Different rotation patterns for each ring
        if i == 0:
            ring.rotation_euler.z = t * math.pi * (2.0 + bass * 0.8)
        elif i == 1:
            ring.rotation_euler.x = t * math.pi * (1.8 + mid * 0.6)
        else:
            ring.rotation_euler.y = t * math.pi * (2.2 + high * 0.7)
        
        add_bezier_keyframe(ring, 'rotation_euler', frame)
        
        # Scaling
        scale = 1.0 + (bass + mid + high) * 0.2
        ring.scale = (scale, scale, scale)
        add_bezier_keyframe(ring, 'scale', frame)

# AMBIENT PARTICLES - Gentle atmospheric movement
ambient_particles = [obj for obj in bpy.data.objects if obj.name.startswith('AmbientParticle')]
for i, particle in enumerate(ambient_particles):
    phase = (i / len(ambient_particles)) * 2 * math.pi
    for frame in range(1, TOTAL_FRAMES + 1, 2):  # Slower for ambient feel
        t = frame / TOTAL_FRAMES
        bass = get_audio('bass', frame, 15)
        mid = get_audio('mid', frame, 12)
        high = get_audio('high', frame, 8)
        
        # Gentle floating motion
        angle = t * math.pi * 0.8 + phase
        original_radius = math.sqrt(particle.location.x**2 + particle.location.y**2)
        radius = original_radius + high * 0.3
        height_offset = math.sin(t * math.pi * 1.5 + phase) * 0.8 + mid * 0.3
        
        original_angle = math.atan2(particle.location.y, particle.location.x)
        new_angle = original_angle + angle * 0.05
        
        particle.location.x = math.cos(new_angle) * radius
        particle.location.y = math.sin(new_angle) * radius
        particle.location.z += height_offset * 0.05
        add_bezier_keyframe(particle, 'location', frame)
        
        # Gentle pulsing
        scale = 1.0 + high * 0.4 + mid * 0.3
        particle.scale = (scale, scale, scale)
        add_bezier_keyframe(particle, 'scale', frame)
        
        # Slow rotation
        particle.rotation_euler = (
            t * math.pi * 1.0 + phase,
            t * math.pi * 0.8 + phase,
            t * math.pi * 1.2 + phase
        )
        add_bezier_keyframe(particle, 'rotation_euler', frame)

print("✅ Highly reactive animations complete")
print(f"   Animated objects: {{len([obj for obj in bpy.data.objects if obj.animation_data])}}")
print(f"   Total keyframes: {{sum([len(obj.animation_data.action.fcurves) if obj.animation_data and obj.animation_data.action else 0 for obj in bpy.data.objects])}}")

# FINAL OPTIMIZATIONS
print("🔧 Applying final commercial optimizations...")

# Viewport optimizations
for obj in bpy.data.objects:
    if obj.type == 'MESH':
        obj.display_type = 'SOLID'
        for mat_slot in obj.material_slots:
            if mat_slot.material:
                mat_slot.material.use_backface_culling = True

# Clear caches
_audio_cache.clear()
_material_cache.clear()

print("✅ Commercial-grade animation system complete!")

# COMMERCIAL OUTPUT CONFIGURATION
print("🎬 Configuring commercial output...")

import os
output_dir = os.path.dirname("/Users/admir/ai/AudioBlenderVideo/output/test_commercial_geometric_tech.blend")
if output_dir:
    os.makedirs(output_dir, exist_ok=True)
    scene.render.filepath = os.path.join(output_dir, "commercial_audio_animation")
    print(f"🎬 Render output set to: {scene.render.filepath}")
else:
    print("⚠️  Warning: No output directory specified")

# SAVE COMMERCIAL BLEND FILE
blend_path = "/Users/admir/ai/AudioBlenderVideo/output/test_commercial_geometric_tech.blend"
print(f"🔍 Saving commercial blend file to: {blend_path}")

if blend_path:
    blend_dir = os.path.dirname(blend_path)
    if blend_dir:
        try:
            os.makedirs(blend_dir, exist_ok=True)
            print(f"✅ Directory created: {blend_dir}")
        except Exception as e:
            print(f"❌ Directory creation error: {e}")
    
    try:
        print("🔍 Saving blend file...")
        bpy.ops.wm.save_as_mainfile(filepath=blend_path)
        print("✅ Save operation completed")
        
        if os.path.exists(blend_path):
            file_size = os.path.getsize(blend_path) / 1024 / 1024
            print("=" * 80)
            print("🎉 COMMERCIAL-GRADE ANIMATION COMPLETE!")
            print("=" * 80)
            print(f"📁 Blend file: {blend_path}")
            print(f"📁 File size: {file_size:.2f} MB")
            print(f"🎬 Render output: {scene.render.filepath}")
            print(f"🎯 Quality: COMMERCIAL BROADCAST")
            print(f"⚡ Features enabled:")
            print(f"   ✅ High-contrast materials with strong emission")
            print(f"   ✅ Dramatic lighting system")
            print(f"   ✅ Proper camera positioning")
            print(f"   ✅ Cycles render engine with high samples")
            print(f"   ✅ Advanced compositor effects")
            print(f"   ✅ Highly reactive animations")
            print(f"   ✅ Commercial-grade color management")
            print("🚀 Ready for commercial rendering!")
            print("=" * 80)
        else:
            print("❌ ERROR: Blend file not created!")
    except Exception as e:
        print(f"❌ Save error: {e}")
else:
    print("❌ ERROR: No blend path specified!")

