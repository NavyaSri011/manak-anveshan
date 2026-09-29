import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { FileText, Upload, Sparkles, Edit3, ArrowRight, Languages, AlertCircle, Loader2 } from 'lucide-react';
import { extractRequirements, extractDocument, analyzeTender } from '../services/api';
import RequirementEditor from '../components/RequirementEditor';

const SAMPLE_TEMPLATES = [
  {
    label: 'BIS Pump — Clear, Cold Water',
    title: 'Horizontal Centrifugal Pump for Clear, Cold Water',
    description: 'Procurement of a horizontal centrifugal pump for clear, cold water in a general-purpose municipal or industrial water-supply application. The pump is intended for continuous service and is rated at 75 kW, 100 m3/hr and 50 m head.',
    techSpec: {
      product_type: 'horizontal centrifugal pump',
      equipment_type: 'horizontal centrifugal rotodynamic pump',
      bis_scope_keywords: 'horizontal centrifugal pumps for clear, cold water; general purpose; other than agricultural and rural water supply',
      application: 'general-purpose municipal and industrial water supply',
      service: 'continuous duty',
      fluid: 'clear, cold water',
      flow_rate: '100 m3/hr',
      head: '50 m',
      power: '75 kW',
      supply_voltage: '415 V',
      frequency: '50 Hz',
      material: 'cast iron casing, stainless steel impeller',
      installation: 'water-supply and water-treatment plant',
      required_characteristics: 'pump performance, hydrostatic pressure, materials, efficiency, marking and testing'
    },
    language: 'en'
  },
  {
    label: 'BIS Pump — Hindi (हिंदी)',
    title: 'साफ, ठंडे पानी के लिए क्षैतिज सेंट्रीफ्यूगल पंप',
    description: 'सामान्य उपयोग वाले नगरपालिका और औद्योगिक जल आपूर्ति के लिए साफ, ठंडे पानी हेतु क्षैतिज सेंट्रीफ्यूगल पंप की खरीद। पंप लगातार संचालन के लिए है और इसकी रेटिंग 90 kW, 120 m3/hr तथा 60 m head है।',
    techSpec: {
      product_type: 'horizontal centrifugal pump',
      equipment_type: 'horizontal centrifugal rotodynamic pump',
      bis_scope_keywords: 'horizontal centrifugal pumps for clear, cold water; general purpose; other than agricultural and rural water supply',
      application: 'general-purpose municipal and industrial water supply',
      service: 'continuous duty',
      fluid: 'clear, cold water',
      flow_rate: '120 m3/hr',
      head: '60 m',
      power: '90 kW',
      supply_voltage: '415 V',
      frequency: '50 Hz',
      installation: 'water-supply and water-treatment plant',
      required_characteristics: 'pump performance, pressure, efficiency, materials, marking and testing'
    },
    language: 'hi'
  },
  {
    label: 'BIS Motor — Three-Phase IE3',
    title: 'Line Operated Three Phase AC Motor — IE3',
    description: 'Procurement of a line-operated three-phase AC motor for industrial drive service, with an IE3 efficiency class, rated 45 kW, 415 V, 50 Hz and 1500 r/min. The motor is intended for general industrial machinery.',
    techSpec: {
      product_type: 'line operated three phase AC motor',
      equipment_type: 'three phase squirrel cage induction motor',
      bis_scope_keywords: 'line operated three phase AC motors; IE Code; efficiency classes and performance specification',
      application: 'industrial machinery and drive systems',
      duty: 'continuous duty',
      phase: 'three phase',
      power: '45 kW',
      voltage: '415 V',
      frequency: '50 Hz',
      speed: '1500 r/min',
      efficiency_class: 'IE3',
      installation: 'industrial machinery',
      required_characteristics: 'rating, efficiency, performance, temperature rise, insulation, vibration, noise, marking and testing'
    },
    language: 'en'
  },
  {
    label: 'BIS LED Street Lighting',
    title: 'LED Street Lighting Luminaire for Road Lighting',
    description: 'Procurement of an outdoor LED street-lighting luminaire for municipal road and street lighting. The luminaire is pole-mounted for roadway illumination and requires electrical safety, photometric performance, protection against dust and moisture, thermal performance and marking.',
    techSpec: {
      product_type: 'LED street lighting luminaire',
      equipment_type: 'luminaire for road and street lighting',
      bis_scope_keywords: 'luminaires part 5 particular requirements section 3 luminaires for road and street lighting; LED street lighting luminaire',
      application: 'municipal road and street lighting',
      mounting: 'roadside pole mounted',
      input_voltage: '230 V AC',
      frequency: '50 Hz',
      power: '120 W',
      light_source: 'LED',
      ingress_protection: 'IP66',
      colour_temperature: '4000 K',
      service: 'continuous outdoor operation',
      environment: 'outdoor roadway',
      required_characteristics: 'electrical safety, photometric performance, dust and moisture protection, thermal performance, mechanical construction and marking'
    },
    language: 'en'
  },
  {
    label: 'BIS Solar PV Module',
    title: 'Crystalline Silicon Terrestrial Photovoltaic (PV) Module',
    description: 'Procurement of crystalline-silicon terrestrial photovoltaic modules for a grid-connected solar PV installation. The procurement item is the PV module itself, with a 540 Wp rating and 1500 V DC maximum system voltage.',
    techSpec: {
      product_type: 'crystalline silicon terrestrial photovoltaic PV module',
      equipment_type: 'Si wafer based terrestrial PV module',
      bis_scope_keywords: 'crystalline silicon terrestrial photovoltaic PV modules; design qualification and type approval; photovoltaic module safety qualification',
      application: 'grid-connected solar photovoltaic power generation',
      technology: 'crystalline silicon, mono PERC',
      module_rating: '540 Wp',
      maximum_system_voltage: '1500 V DC',
      environment: 'outdoor terrestrial installation',
      system_type: 'grid connected',
      service: 'continuous outdoor operation',
      required_characteristics: 'electrical performance, design qualification, type approval, construction safety, testing and marking'
    },
    language: 'en'
  }
];

export default function NewAnalysis() {
  const navigate = useNavigate();

  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [techSpec, setTechSpec] = useState({});
  const [techSpecText, setTechSpecText] = useState('');
  const [language, setLanguage] = useState('en');
  const [uploadedFile, setUploadedFile] = useState(null);

  const [extractedData, setExtractedData] = useState(null);
  const [isExtracting, setIsExtracting] = useState(false);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [errorMsg, setErrorMsg] = useState(null);

  // Load sample template
  const applyTemplate = (tpl) => {
    setTitle(tpl.title);
    setDescription(tpl.description);
    setTechSpec(tpl.techSpec);
    setTechSpecText(JSON.stringify(tpl.techSpec, null, 2));
    setLanguage(tpl.language);
    setUploadedFile(null);
    setExtractedData(null);
    setErrorMsg(null);
  };

  // Document File Upload Parsing
  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (!file) return;
    setUploadedFile(file);

    // Remove stale pump / sample JSON immediately when a new document is uploaded
    setTechSpec({});
    setTechSpecText('');
    setExtractedData(null);
    setErrorMsg(null);

    // Pre-populate title & description from document filename if generic or empty
    const cleanName = file.name.replace(/\.[^/.]+$/, "").replace(/[-_]/g, " ");
    if (!title.trim() || title.toLowerCase().includes('pump') || title.toLowerCase().includes('motor')) {
      setTitle(cleanName);
    }
    setDescription(`Document specification uploaded from file: ${file.name}`);
  };

  // Extract Requirements preview
  const handleExtractRequirements = async () => {
    if (!title.trim() && !uploadedFile) {
      setErrorMsg('Please enter a Tender / Product Title or upload a document first.');
      return;
    }
    setErrorMsg(null);
    setIsExtracting(true);

    try {
      let res;
      if (uploadedFile) {
        const formData = new FormData();
        formData.append('file', uploadedFile);
        if (title.trim()) {
          formData.append('product_title', title);
        }
        formData.append('language', language);
        res = await extractDocument(formData);
      } else {
        let parsedSpec = techSpec;
        if (techSpecText.trim()) {
          try {
            parsedSpec = JSON.parse(techSpecText);
          } catch {
            parsedSpec = {};
            techSpecText.split('\n').forEach(line => {
              const parts = line.split(':');
              if (parts.length >= 2) {
                parsedSpec[parts[0].trim()] = parts.slice(1).join(':').trim();
              }
            });
          }
        }

        res = await extractRequirements({
          product_title: title,
          product_description: description,
          technical_specification: parsedSpec,
          language: language
        });
      }

      if (res.product && res.product.name && (!title || title === uploadedFile?.name)) {
        setTitle(res.product.name);
      }

      const extractedParams = res.technical_parameters || {};
      setExtractedData(res);
      setTechSpec(extractedParams);
      setTechSpecText(JSON.stringify(extractedParams, null, 2));

      if (Object.keys(extractedParams).length === 0) {
        setErrorMsg('No technical parameters detected in the document. You may manually add parameters below.');
      }
    } catch (err) {
      console.error('Extraction error:', err);
      setErrorMsg(err.response?.data?.detail || err.message || 'Failed to extract requirements. Check backend connection.');
      setExtractedData(null);
    } finally {
      setIsExtracting(false);
    }
  };

  // Full Analysis execution
  const handleRunAnalysis = async (e) => {
    e.preventDefault();
    if (!title.trim()) {
      setErrorMsg('Please provide a Tender / Product Title.');
      return;
    }

    setErrorMsg(null);
    setIsAnalyzing(true);

    try {
      let parsedSpec = techSpec;
      if (techSpecText.trim() && Object.keys(techSpec).length === 0) {
        try {
          parsedSpec = JSON.parse(techSpecText);
        } catch {
          parsedSpec = {};
          techSpecText.split('\n').forEach(line => {
            const parts = line.split(':');
            if (parts.length >= 2) {
              parsedSpec[parts[0].trim()] = parts.slice(1).join(':').trim();
            }
          });
        }
      }

      const payload = {
        request_id: `TENDER-2026-${Math.floor(1000 + Math.random() * 9000)}`,
        product_title: title,
        product_description: description,
        technical_specification: parsedSpec,
        language: language,
        document_text: uploadedFile ? `File: ${uploadedFile.name}` : ''
      };

      const response = await analyzeTender(payload);
      
      // Navigate to results page passing state
      navigate('/results', { state: { resultData: response } });
    } catch (err) {
      console.error('Analysis error:', err);
      setErrorMsg('Failed to run analysis. Please check API backend status.');
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
      
      {/* Page Title */}
      <div className="border-b border-slate-300 pb-4">
        <h1 className="text-2xl font-bold text-slate-900 font-serif flex items-center gap-2">
          <FileText className="w-6 h-6 text-amber-600" />
          New Procurement Tender Analysis
        </h1>
        <p className="text-xs text-slate-600 mt-1">
          Input tender title, product description, or upload procurement PDF/DOCX to extract specifications and identify matching Indian Standards.
        </p>
      </div>

      {/* Error Alert */}
      {errorMsg && (
        <div className="bg-rose-50 border border-rose-300 rounded p-4 text-xs text-rose-900 flex items-center space-x-2">
          <AlertCircle className="w-5 h-5 text-rose-600 shrink-0" />
          <span>{errorMsg}</span>
        </div>
      )}

      {/* Sample Templates Bar */}
      <div className="bg-slate-100 border border-slate-300 rounded p-3 text-xs">
        <span className="font-bold text-slate-700 uppercase text-[11px] block mb-2">
          Quick Demo Presets:
        </span>
        <div className="flex flex-wrap gap-2">
          {SAMPLE_TEMPLATES.map((tpl, i) => (
            <button
              key={i}
              type="button"
              onClick={() => applyTemplate(tpl)}
              className="bg-white hover:bg-slate-900 hover:text-white text-slate-800 border border-slate-300 font-medium px-3 py-1.5 rounded transition text-[11px]"
            >
              {tpl.label}
            </button>
          ))}
        </div>
      </div>

      <form onSubmit={handleRunAnalysis} className="space-y-6">
        
        {/* Top Controls Grid */}
        <div className="bg-white border border-slate-300 rounded-lg p-6 space-y-4">
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {/* Tender Title */}
            <div className="md:col-span-2 space-y-1">
              <label className="text-xs font-bold text-slate-800 uppercase tracking-wider">
                Tender / Product Title <span className="text-rose-600">*</span>
              </label>
              <input
                type="text"
                required
                placeholder="e.g. Horizontal Centrifugal Pump for Water Supply"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                className="w-full bg-slate-50 border border-slate-300 rounded px-3 py-2 text-xs text-slate-900 focus:outline-hidden focus:border-amber-600 font-medium"
              />
            </div>

            {/* Language Selection */}
            <div className="space-y-1">
              <label className="text-xs font-bold text-slate-800 uppercase tracking-wider flex items-center gap-1">
                <Languages className="w-3.5 h-3.5 text-slate-600" />
                Query Language
              </label>
              <select
                value={language}
                onChange={(e) => setLanguage(e.target.value)}
                className="w-full bg-slate-50 border border-slate-300 rounded px-3 py-2 text-xs text-slate-900 focus:outline-hidden focus:border-amber-600 font-medium"
              >
                <option value="en">English (en)</option>
                <option value="hi">Hindi / हिन्दी (hi)</option>
                <option value="ta">Tamil / தமிழ் (ta)</option>
                <option value="mr">Marathi / मराठी (mr)</option>
              </select>
            </div>
          </div>

          {/* Product Description */}
          <div className="space-y-1">
            <label className="text-xs font-bold text-slate-800 uppercase tracking-wider">
              Product Scope & Technical Description
            </label>
            <textarea
              rows={3}
              placeholder="Describe operating environment, fluid parameters, installation requirements, or natural language search query..."
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="w-full bg-slate-50 border border-slate-300 rounded px-3 py-2 text-xs text-slate-900 focus:outline-hidden focus:border-amber-600"
            />
          </div>

          {/* Document Upload Mock */}
          <div className="border-2 border-dashed border-slate-300 rounded-lg p-4 text-center bg-slate-50/50 hover:bg-slate-100/50 transition cursor-pointer relative">
            <input
              type="file"
              accept=".pdf,.docx,.txt"
              onChange={handleFileUpload}
              className="absolute inset-0 opacity-0 cursor-pointer w-full h-full"
            />
            <div className="flex flex-col items-center justify-center space-y-1">
              <Upload className="w-6 h-6 text-slate-500" />
              <div className="text-xs font-semibold text-slate-700">
                {uploadedFile ? `Attached: ${uploadedFile.name}` : 'Click to Upload Tender PDF / DOCX Specification Document'}
              </div>
              <div className="text-[11px] text-slate-500">
                Extracts technical parameters & IS references automatically
              </div>
            </div>
          </div>

          {/* Technical Specification JSON / Text */}
          <div className="space-y-1">
            <label className="text-xs font-bold text-slate-800 uppercase tracking-wider flex justify-between">
              <span>Technical Specification Key-Values / JSON</span>
              <span className="text-[10px] text-slate-500 font-mono">e.g. flow_rate: 100 m3/hr</span>
            </label>
            <textarea
              rows={4}
              placeholder={'{\n  "flow_rate": "100 m3/hr",\n  "head": "50 m",\n  "power": "75 kW"\n}'}
              value={techSpecText}
              onChange={(e) => {
                const text = e.target.value;
                setTechSpecText(text);
                try {
                  const parsed = JSON.parse(text);
                  setTechSpec(parsed);
                  if (extractedData) {
                    setExtractedData({
                      ...extractedData,
                      technical_parameters: parsed
                    });
                  }
                } catch {
                  // transient JSON syntax state
                }
              }}
              className="w-full bg-slate-900 text-slate-100 border border-slate-700 rounded px-3 py-2 text-xs font-mono focus:outline-hidden focus:border-amber-500"
            />
          </div>

          {/* Extract Requirements Trigger Button */}
          <div className="flex justify-end">
            <button
              type="button"
              onClick={handleExtractRequirements}
              disabled={isExtracting}
              className="bg-slate-800 hover:bg-slate-900 text-slate-100 font-bold px-4 py-2 rounded text-xs flex items-center space-x-2 transition"
            >
              {isExtracting ? (
                <Loader2 className="w-4 h-4 animate-spin text-amber-400" />
              ) : (
                <Sparkles className="w-4 h-4 text-amber-400" />
              )}
              <span>{isExtracting ? 'Extracting Parameters...' : 'Extract & Preview Requirements'}</span>
            </button>
          </div>

        </div>

        {/* Extracted Requirements Interactive Preview Editor */}
        {extractedData && (
          <RequirementEditor
            extracted={extractedData}
            onRequirementsUpdated={(updated) => {
              setTechSpec(updated);
              setTechSpecText(JSON.stringify(updated, null, 2));
              setExtractedData({
                ...extractedData,
                technical_parameters: updated
              });
            }}
          />
        )}

        {/* Form Action Submit */}
        <div className="flex justify-between items-center bg-slate-900 text-white p-4 rounded-lg border-t-2 border-amber-600">
          <div className="text-xs text-slate-300">
            Clicking Analyze will run hybrid retrieval, QCO checks, version lifecycle audits, and graph generation.
          </div>
          <button
            type="submit"
            disabled={isAnalyzing}
            className="bg-amber-600 hover:bg-amber-700 text-slate-950 font-bold px-6 py-2.5 rounded text-xs flex items-center space-x-2 transition shadow-md cursor-pointer"
          >
            {isAnalyzing ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin text-slate-950" />
                <span>Processing Analysis...</span>
              </>
            ) : (
              <>
                <span>Analyze Indian Standards</span>
                <ArrowRight className="w-4 h-4" />
              </>
            )}
          </button>
        </div>

      </form>

    </div>
  );
}
